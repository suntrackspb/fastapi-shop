from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import EmailStr, validator, AnyHttpUrl
import secrets
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Store API"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/store_db")

    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    RATE_LIMIT_PER_HOUR: int = 1000

    # Cache
    CACHE_TTL_HOURS: int = 12

    # Email
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "True").lower() == "true"
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAILS_FROM_EMAIL: str = os.getenv("EMAILS_FROM_EMAIL", "")
    EMAILS_FROM_NAME: str = os.getenv("EMAILS_FROM_NAME", "Store Admin")

    # Media
    MEDIA_ROOT: str = "media"
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "5242880"))  # 5MB

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Admin user
    FIRST_ADMIN_EMAIL: str = os.getenv("FIRST_ADMIN_EMAIL", "admin@example.com")
    FIRST_ADMIN_PASSWORD: str = os.getenv("FIRST_ADMIN_PASSWORD", "admin123")
    FIRST_ADMIN_FULL_NAME: str = os.getenv("FIRST_ADMIN_FULL_NAME", "Admin User")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 