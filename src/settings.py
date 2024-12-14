from pathlib import Path

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    video_path: Path


app_settings = AppSettings(
    _env_file=f'{__file__}/../.env',
)
