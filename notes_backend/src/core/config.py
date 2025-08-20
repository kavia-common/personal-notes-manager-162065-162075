import functools
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Provides database credentials, JWT configuration, and CORS settings.
    """

    # Database
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")
    POSTGRES_DB: str = Field(default="notes_db", description="PostgreSQL database name")
    POSTGRES_USER: str = Field(default="notes_user", description="PostgreSQL user")
    POSTGRES_PASSWORD: str = Field(default="password", description="PostgreSQL password")

    # JWT
    JWT_SECRET_KEY: str = Field(default="CHANGE_ME", description="Secret key for JWT")
    JWT_ALGORITHM: str = Field(default="HS256", description="Algorithm for JWT")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24, description="Token expiration in minutes")

    # CORS
    CORS_ALLOW_ORIGINS: str = Field(default="*", description="Comma separated allowed origins")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    @property
    def database_url(self) -> str:
        """Build SQLAlchemy database URL for PostgreSQL."""
        user = self.POSTGRES_USER
        pwd = self.POSTGRES_PASSWORD
        host = self.POSTGRES_HOST
        port = self.POSTGRES_PORT
        db = self.POSTGRES_DB
        return f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db}"

    @property
    def cors_allow_origins(self) -> List[str]:
        """Return list of allowed CORS origins."""
        raw = self.CORS_ALLOW_ORIGINS
        if not raw:
            return ["*"]
        return [o.strip() for o in raw.split(",") if o.strip()]


@functools.lru_cache()
# PUBLIC_INTERFACE
def get_settings() -> Settings:
    """Get cached application settings loaded from environment variables."""
    return Settings()
