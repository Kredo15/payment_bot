from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: SecretStr
    DB_NAME: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg:" \
               f"//{self.DB_USER}:" \
               f"{self.DB_PASS.get_secret_value()}" \
               f"@{self.DB_HOST}:" \
               f"{self.DB_PORT}/" \
               f"{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env", env_file_encoding="utf8", extra="ignore")


class Settings(BaseSettings):
    MODE: str
    API_KEY_BOT: str
    ADMIN: int

    db_settings: DBSettings = DBSettings()

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env", env_file_encoding="utf8", extra="ignore")


settings = Settings()
