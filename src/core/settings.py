import os
import secrets
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DevelopmentSettings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    API_HOST: str = "localhost"
    API_PORT: int = 8000

    # Redis
    REDIS_HOST: str
    REDIS_DB: int = 0
    REDIS_USERNAME: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None

    # Postgres
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = str(5432)

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, 'envs/.env.example'))


class TestingSettings(DevelopmentSettings):
    ...


class ProductionSettings(DevelopmentSettings):

    class Config:
        model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, 'envs/.env.prod'))


settings = DevelopmentSettings()
