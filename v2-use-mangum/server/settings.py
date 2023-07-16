from pathlib import Path
from typing import Tuple, Type

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

print(Path(__file__).resolve().parent / ".env.local")


class Settings(BaseSettings):
    DEBUG: bool = False
    DB_URL: str = PostgresDsn

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        # first item is highest priority
        return env_settings, dotenv_settings, init_settings

    class Config:
        env_file = Path(__file__).resolve().parent / ".env.local"


settings = Settings()
