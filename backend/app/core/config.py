from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Falcon Vision API"
    environment: str = "development"
    debug: bool = True

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "falcon_vision"

    jwt_secret_key: str = Field(default="change-this-secret-before-production")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    upload_dir: Path = Path("uploads")
    max_pdf_size_mb: int = 25
    max_face_image_size_mb: int = 10

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
