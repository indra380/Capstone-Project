from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_opaque_token() -> str:
    return secrets.token_urlsafe(48)


def create_access_token(
    subject: str,
    role: str | None = None,
    roles: list[str] | None = None,
    session_key: str | None = None,
    expires_minutes: int = 0,
) -> str:
    settings = get_settings()
    secret = settings.jwt_secret_key
    ttl_minutes = expires_minutes or settings.access_token_expire_minutes
    now = datetime.now(timezone.utc)
    role_values = roles or ([] if role is None else [role])
    primary_role = role_values[0] if role_values else "viewer"
    payload = {
        "sub": subject,
        "role": primary_role,
        "roles": role_values,
        "type": "access",
        "sid": session_key,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ttl_minutes)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str, session_key: str, expires_minutes: int = 0) -> str:
    settings = get_settings()
    secret = settings.jwt_secret_key
    ttl_minutes = expires_minutes or settings.refresh_token_expire_minutes
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "type": "refresh",
        "sid": session_key,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ttl_minutes)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str, expected_type: str | None = None) -> dict[str, Any]:
    settings = get_settings()
    secret = settings.jwt_secret_key
    try:
        data = jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])
        if not isinstance(data, dict):
            raise JWTError("Invalid payload")
        if expected_type and data.get("type") != expected_type:
            raise JWTError("Invalid token type")
        return data
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


def decode_access_token(token: str) -> dict[str, Any]:
    return decode_token(token, expected_type="access")


def decode_refresh_token(token: str) -> dict[str, Any]:
    return decode_token(token, expected_type="refresh")


def get_current_identity(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict[str, Any]:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")
    return decode_access_token(credentials.credentials)
