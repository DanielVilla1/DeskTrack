from enum import StrEnum
from functools import lru_cache
from typing import Annotated

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

API_V1_PREFIX = "/api/v1"


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # SecretStr keeps the password out of repr() and logs.
    database_url: SecretStr
    # Defaults to production so a missing variable never exposes /docs.
    environment: Environment = Environment.PRODUCTION
    # NoDecode keeps pydantic-settings from expecting JSON for this list.
    cors_origins: Annotated[list[str], NoDecode]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
