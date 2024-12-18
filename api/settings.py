import sys

from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    test: bool = Field("pytest" in sys.modules, validation_alias="TEST")
    db_name: str = Field("augmenta", validation_alias="DB_DATABASE")
    db_user: str = Field("postgres", validation_alias="DB_USER")
    db_password: str = Field("", validation_alias="DB_PASSWORD")
    db_host: str = Field("127.0.0.1", validation_alias="DB_HOST")
    db_port: int = Field(5432, validation_alias="DB_PORT")
    openai_api_key: str = Field("", validation_alias="OPENAI_API_KEY")

    model_config = SettingsConfigDict(env_file="conf/.env", extra="ignore")

    @field_validator("db_name", mode="before")
    @classmethod
    def set_db_name(cls, db, info: ValidationInfo):
        if info.data["test"]:
            return "augmenta_test"
        return db

    @property
    def connection_str(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
