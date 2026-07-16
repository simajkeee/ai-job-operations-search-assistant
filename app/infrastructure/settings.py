from typing import Literal

from functools import lru_cache
from pydantic import SecretStr, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str
    jwt_secret_key: SecretStr
    jwt_algorithm: Literal["HS256"] = "HS256"
    jwt_access_token_expire_minutes: PositiveInt = 30
    openai_api_key: SecretStr | None = None


@lru_cache
def get_settings() -> Settings:
    # BaseSettings loads required values from environment at runtime.
    return Settings()  # type: ignore[call-arg]
