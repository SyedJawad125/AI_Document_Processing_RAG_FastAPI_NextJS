# from pydantic_settings import BaseSettings
# from pydantic import Field, AnyUrl, validator
# from typing import Optional
# import warnings

# class Settings(BaseSettings):
#     # Database configuration (using AnyUrl instead of PostgresDsn)
#     SQLALCHEMY_DATABASE_URL: str = Field(
#         default="postgresql+psycopg2://postgres:admin@localhost:5432/FastApi_NextJs_PostgreSql_SignUp_Login_Template",
#         description="PostgreSQL connection URL"
#     )
    
#     # Add validator to ensure it's a PostgreSQL URL
#     @validator('SQLALCHEMY_DATABASE_URL')
#     def validate_db_url(cls, v):
#         if not v.startswith('postgresql'):
#             warnings.warn(f"Using non-PostgreSQL database: {v}", RuntimeWarning)
#         return v
    
#     # Authentication
#     SECRET_KEY: str = Field(
#         default="this-is-a-very-secure-32-char-secret-key-1234",
#         min_length=32,
#         max_length=128
#     )
#     ALGORITHM: str = Field(default="HS256")
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)
    
#     # Optional configurations
#     EMAIL_HOST: Optional[str] = None
#     EMAIL_PORT: Optional[int] = None
#     EMAIL_USE_SSL: Optional[bool] = None
#     EMAIL_USER: Optional[str] = None
#     EMAIL_PASSWORD: Optional[str] = None
#     ADMIN_EMAIL: Optional[str] = None
    
#     REDIS_HOST: Optional[str] = None
#     REDIS_PORT: Optional[int] = None
#     REDIS_DB: Optional[int] = None
#     REDIS_CACHE_TTL: Optional[int] = None

#     class Config:
#         env_file = ".env"
#         env_file_encoding = 'utf-8'
#         extra = "ignore"

# settings = Settings()




"""
app/core/config.py
──────────────────
All application settings are loaded here from .env using pydantic-settings.
Import `settings` anywhere in the app — never use os.environ directly.

Why pydantic-settings?
  - Type validation at startup (wrong type = instant crash, not silent bug)
  - Auto-reads from .env file
  - Works perfectly with FastAPI's dependency injection
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )

    # ── App ────────────────────────────────────────────────────────
    APP_NAME:    str  = 'AI Document Processing System'
    ENVIRONMENT: str  = 'development'
    DEBUG:       bool = False

    # ── Auth ───────────────────────────────────────────────────────
    SECRET_KEY:                    str = 'changeme-use-a-real-secret-in-production'
    ALGORITHM:                     str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES:   int = 600
    REFRESH_TOKEN_EXPIRE_DAYS:     int = 15

    # ── URLs ───────────────────────────────────────────────────────
    BACKEND_BASE_URL:  str = 'http://localhost:8000'
    FRONTEND_BASE_URL: str = 'http://localhost:5173'

    # ── Database ───────────────────────────────────────────────────
    POSTGRES_DB:       str = 'document_ai'
    POSTGRES_USER:     str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_HOST:     str = 'db'
    POSTGRES_PORT:     int = 5432

    DATABASE_URL:      str = 'postgresql+asyncpg://postgres:postgres@db:5432/document_ai'
    SYNC_DATABASE_URL: str = 'postgresql+psycopg://postgres:postgres@db:5432/document_ai'

    # ── Groq LLM ───────────────────────────────────────────────────
    GROQ_API_KEY: str = ''
    GROQ_MODEL:   str = 'llama-3.1-8b-instant'
    GROQ_TIMEOUT: int = 60

    # ── Embeddings ─────────────────────────────────────────────────
    EMBEDDING_MODEL:     str = 'sentence-transformers/all-MiniLM-L6-v2'
    EMBEDDING_DIMENSION: int = 384

    # ── RAG ────────────────────────────────────────────────────────
    CHUNK_SIZE:          int   = 800
    CHUNK_OVERLAP:       int   = 150
    TOP_K:               int   = 5
    RELEVANCE_THRESHOLD: float = 0.3

    # ── Files ──────────────────────────────────────────────────────
    UPLOAD_DIR:       str = 'uploads'
    REPORT_DIR:       str = 'reports'
    MAX_FILE_SIZE_MB: int = 20

    # ── Logging ────────────────────────────────────────────────────
    LOG_LEVEL: str = 'INFO'

    # ── Computed helpers ───────────────────────────────────────────
    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    @property
    def allowed_origins(self) -> list[str]:
        return [
            self.FRONTEND_BASE_URL,
            'http://localhost:3000',
            'http://localhost:5173',
        ]

    # Optional configurations
    EMAIL_HOST: Optional[str] = None
    EMAIL_PORT: Optional[int] = None
    EMAIL_USE_SSL: Optional[bool] = None
    EMAIL_USER: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None
    ADMIN_EMAIL: Optional[str] = None
    
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = None
    REDIS_DB: Optional[int] = None
    REDIS_CACHE_TTL: Optional[int] = None


@lru_cache           # Singleton — only parsed once
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
# Additional validation
if not settings.SQLALCHEMY_DATABASE_URL.startswith('postgresql'):
    raise ValueError("Only PostgreSQL database is supported")