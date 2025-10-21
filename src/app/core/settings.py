from functools import cached_property
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application-level settings."""

    model_config = SettingsConfigDict(env_prefix="APP_")

    NAME: str = "Callyfy"
    VERSION: str = "0.1.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DBSettings(BaseSettings):
    """Database settings."""

    model_config = SettingsConfigDict(env_prefix="DB_")

    PATH: str = "callyfy.db"
    ECHO: bool = False
    FUTURE: bool = True

    @cached_property
    def url(self) -> str:
        """Get the database URL."""
        return f"sqlite+aiosqlite:///{self.PATH}"


class PathsSettings(BaseSettings):
    """Filesystem layout for storing meeting artifacts."""

    model_config = SettingsConfigDict(env_prefix="PATHS_")

    DATA_DIR: Path = Path("data")
    AUDIO_DIR_NAME: str = "audio"
    SCREEN_DIR_NAME: str = "screens"


class Settings(BaseSettings):
    """Root settings aggregating all configuration sections."""

    model_config = SettingsConfigDict(env_file=".env")

    app: AppSettings = Field(default_factory=AppSettings)
    db: DBSettings = Field(default_factory=DBSettings)
    paths: PathsSettings = Field(default_factory=PathsSettings)
