from functools import cached_property
from pathlib import Path
from typing import Literal
from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # core sqlalchemy settings
    MAIN_DB_NAME: str
    MAIN_DB_USER: str
    MAIN_DB_PASSWD: str
    MAIN_DB_PORT: int
    MAIN_DB_HOST: str

    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASSWD: str
    TEST_DB_PORT: int
    TEST_DB_HOST: str
    TOKEN: str
    DEBUG_TOKEN: str

    ENVIRONMENT: Literal["DEV", "PRD"] = "DEV"

    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env", case_sensitive=True
    )

    @computed_field
    @cached_property
    def MAIN_DB_URI(self) -> str:  # pylint: disable=invalid-name
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                username=self.MAIN_DB_USER,
                password=self.MAIN_DB_PASSWD,
                host=self.MAIN_DB_HOST,
                port=self.MAIN_DB_PORT,
                path=self.MAIN_DB_NAME,
            )
        )

    @computed_field
    @cached_property
    def TEST_DB_URI(self) -> str:  # pylint: disable=invalid-name
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                username=self.TEST_DB_USER,
                password=self.TEST_DB_PASSWD,
                host=self.TEST_DB_HOST,
                port=self.TEST_DB_PORT,
                path=self.TEST_DB_NAME,
            )
        )

    @computed_field
    @cached_property
    def SQLITE_DB_URI(self) -> str:  # pylint: disable=invalid-name
        return str(
            MultiHostUrl.build(
                scheme="sqlite+aiosqlite",
                host="",
                path="database/vegacord.sqlite",
            )
        )


settings: Settings = Settings()
