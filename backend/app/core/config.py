from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Project Manager API"
    app_env: str = "development"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./project15.db"
    cors_origins: str = "http://localhost:3000"
    scheduler_interval_minutes: int = 60
    default_report_cadence: str = "daily"
    ai_provider: str = "openai"
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str = ""
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    gemini_model: str = "gemini-1.5-pro"
    gemini_api_key: str = ""
    ai_timeout_seconds: int = 20
    notification_webhook_url: str = ""
    notification_timeout_seconds: int = 10
    jwt_secret_key: str = "dev-secret-key-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    refresh_token_expire_minutes: int = 10080
    account_lock_threshold: int = 5
    account_lock_minutes: int = 30
    password_reset_expire_minutes: int = 30
    email_verification_expire_minutes: int = 1440
    session_expire_minutes: int = 10080

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
