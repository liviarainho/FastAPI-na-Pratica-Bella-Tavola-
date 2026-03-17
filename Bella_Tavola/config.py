from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Bella Tavola API", validation_alias="APP_NAME")
    app_version: str = Field(default="1.0.0", validation_alias="APP_VERSION")
    app_description: str = Field(
        default="API do restaurante Bella Tavola",
        validation_alias="APP_DESCRIPTION",
    )
    debug: bool = Field(
        default=False,
        validation_alias=AliasChoices("APP_DEBUG", "DEBUG"),
    )
    max_mesas: int = Field(default=20, validation_alias="MAX_MESAS")
    max_pessoas_por_mesa: int = Field(
        default=10,
        validation_alias="MAX_PESSOAS_POR_MESA",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
