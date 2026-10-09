from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from app.api.deps import db_session
from app.core.auth import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    generate_opaque_token,
    get_current_identity,
    hash_password,
    hash_token,
    verify_password,
)
from app.core.config import get_settings
from app.core.security import get_current_user
from app.models.entities import (
    EmailVerificationToken,
    PasswordResetToken,
    ProjectMember,
    RefreshTokenEntity,
    RoleEntity,
    SessionEntity,
    UserAccount,
    UserRole,
)
from app.schemas.api import (
    AuthResponse,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    SessionOut,
    TokenOut,
)
from app.services import audit

router = APIRouter(tags=["auth"])


def _resolve_user_roles(session: Session, user_id: int, fallback: str) -> list[str]:
    links = session.exec(select(UserRole).where(UserRole.user_id == user_id)).all()
    if not links:
        return [fallback]
    role_ids = [link.role_id for link in links]
    roles = session.exec(select(RoleEntity).where(RoleEntity.id.in_(role_ids))).all()
    values = [row.name for row in roles]
    return values or [fallback]


def _create_auth_response(
    session: Session,
    user: UserAccount,
    request: Request,
    role_fallback: str,
) -> AuthResponse:
    settings = get_settings()
    roles = _resolve_user_roles(session, user.id, role_fallback)
    session_key = generate_opaque_token()
    access_token = create_access_token(subject=str(user.id), roles=roles, session_key=session_key)
    refresh_token = create_refresh_token(subject=str(user.id), session_key=session_key)

    user_session = SessionEntity(
        user_id=user.id,
        session_key=session_key,
        ip_address=request.client.host if request.client else "",
        user_agent=request.headers.get("user-agent", ""),
        expires_at=datetime.now(UTC) + timedelta(minutes=settings.session_expire_minutes),
    )
    session.add(user_session)
    session.commit()
    session.refresh(user_session)

    refresh_row = RefreshTokenEntity(
        user_id=user.id,
        session_id=user_session.id,
        token_hash=hash_token(refresh_token),
        expires_at=datetime.now(UTC) + timedelta(minutes=settings.refresh_token_expire_minutes),
    )
    session.add(refresh_row)
    session.commit()

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        session_id=user_session.session_key,
        roles=roles,
    )


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
@router.post("/auth/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def register(payload: RegisterRequest, session: Session = Depends(db_session)):
    existing = session.exec(select(UserAccount).where(UserAccount.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = UserAccount(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    role_row = session.exec(select(RoleEntity).where(RoleEntity.name == payload.role)).first()
    if role_row:
        session.add(UserRole(user_id=user.id, role_id=role_row.id))
        session.commit()

    token = create_access_token(subject=str(user.id), role=user.role, roles=[payload.role])
    return TokenOut(access_token=token)


@router.post("/login", response_model=AuthResponse)
@router.post("/auth/login", response_model=AuthResponse, include_in_schema=False)
def login(payload: LoginRequest, request: Request, session: Session = Depends(db_session)):
    settings = get_settings()
    user = session.exec(select(UserAccount).where(UserAccount.email == payload.email)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.locked_until and user.locked_until > datetime.now(UTC):
        raise HTTPException(status_code=423, detail="Account is temporarily locked")
    if not verify_password(payload.password, user.password_hash):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= settings.account_lock_threshold:
            user.locked_until = datetime.now(UTC) + timedelta(minutes=settings.account_lock_minutes)
        session.add(user)
        session.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user.failed_login_attempts = 0
    user.locked_until = None
    session.add(user)
    session.commit()

    result = _create_auth_response(session, user, request, user.role)
    audit.log_action(
        session,
        actor_role=user.role,
        actor_user_id=user.id,
        ip_address=request.client.host if request.client else "",
        action="user_login",
        entity_type="user",
        entity_id=str(user.id),
        rationale="User login successful",
    )
    return result


@router.post("/refresh", response_model=AuthResponse)
def refresh_token(payload: RefreshTokenRequest, request: Request, session: Session = Depends(db_session)):
    data = decode_refresh_token(payload.refresh_token)
    token_hash = hash_token(payload.refresh_token)
    token_row = session.exec(select(RefreshTokenEntity).where(RefreshTokenEntity.token_hash == token_hash)).first()
    if token_row is None or token_row.revoked_at is not None or token_row.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=401, detail="Refresh token is invalid")

    user = session.get(UserAccount, int(data.get("sub")))
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User is inactive")

    token_row.revoked_at = datetime.now(UTC)
    session.add(token_row)
    session.commit()

    return _create_auth_response(session, user, request, user.role)


@router.post("/logout")
def logout(
    payload: RefreshTokenRequest,
    request: Request,
    identity: dict = Depends(get_current_identity),
    session: Session = Depends(db_session),
):
    token_hash = hash_token(payload.refresh_token)
    token_row = session.exec(select(RefreshTokenEntity).where(RefreshTokenEntity.token_hash == token_hash)).first()
    if token_row:
        token_row.revoked_at = datetime.now(UTC)
        session.add(token_row)
        user_session = session.get(SessionEntity, token_row.session_id)
        if user_session:
            user_session.is_active = False
            session.add(user_session)
        session.commit()

    audit.log_action(
        session,
        actor_role=str(identity.get("role", "viewer")),
        actor_user_id=int(identity.get("sub", 0)) if identity.get("sub") else None,
        ip_address=request.client.host if request.client else "",
        action="user_logout",
        entity_type="session",
        entity_id=str(identity.get("sid", "")),
        rationale="User logout",
    )
    return {"ok": True}


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, session: Session = Depends(db_session)):
    settings = get_settings()
    user = session.exec(select(UserAccount).where(UserAccount.email == payload.email)).first()
    if user is None:
        return {"ok": True, "message": "If the account exists, reset instructions will be sent."}

    raw = generate_opaque_token()
    reset = PasswordResetToken(
        user_id=user.id,
        token_hash=hash_token(raw),
        expires_at=datetime.now(UTC) + timedelta(minutes=settings.password_reset_expire_minutes),
    )
    session.add(reset)
    session.commit()
    return {
        "ok": True,
        "message": "Password reset token generated (email provider integration pending).",
        "reset_token": raw,
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, session: Session = Depends(db_session)):
    row = session.exec(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == hash_token(payload.token))
    ).first()
    if row is None or row.used_at is not None or row.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Reset token is invalid or expired")
    user = session.get(UserAccount, row.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(payload.new_password)
    user.password_changed_at = datetime.now(UTC)
    user.failed_login_attempts = 0
    user.locked_until = None
    row.used_at = datetime.now(UTC)
    session.add(user)
    session.add(row)
    session.commit()
    return {"ok": True}


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    user: UserAccount = Depends(get_current_user),
    session: Session = Depends(db_session),
):
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    user.password_hash = hash_password(payload.new_password)
    user.password_changed_at = datetime.now(UTC)
    session.add(user)
    session.commit()
    return {"ok": True}


@router.post("/verify-email")
def verify_email(token: str, session: Session = Depends(db_session)):
    row = session.exec(
        select(EmailVerificationToken).where(EmailVerificationToken.token_hash == hash_token(token))
    ).first()
    if row is None or row.used_at is not None or row.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Verification token is invalid or expired")
    user = session.get(UserAccount, row.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.email_verified = True
    row.used_at = datetime.now(UTC)
    session.add(user)
    session.add(row)
    session.commit()
    return {"ok": True}


@router.get("/sessions", response_model=list[SessionOut])
def list_sessions(
    user: UserAccount = Depends(get_current_user),
    session: Session = Depends(db_session),
):
    rows = session.exec(select(SessionEntity).where(SessionEntity.user_id == user.id)).all()
    return [
        SessionOut(
            session_id=row.session_key,
            ip_address=row.ip_address,
            user_agent=row.user_agent,
            is_active=row.is_active,
            last_seen_at=row.last_seen_at,
            expires_at=row.expires_at,
        )
        for row in rows
    ]
