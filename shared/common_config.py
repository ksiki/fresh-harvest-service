from datetime import timedelta
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    x_api_key: str
    database_url: str
    rabbitmq_url: str
    s3_endpoint_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket_name: str
    database_schema: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class Constants(BaseSettings):
    archive_lifetime: timedelta


settings: Final[Settings] = Settings()
constants: Final[Constants] = Constants(archive_lifetime=timedelta(hours=168))
