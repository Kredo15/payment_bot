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
        return (
            f"postgresql+asyncpg:"
            f"//{self.DB_USER}:"
            f"{self.DB_PASS.get_secret_value()}"
            f"@{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env", env_file_encoding="utf8", extra="ignore"
    )


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env", env_file_encoding="utf8", extra="ignore"
    )

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


class CryptoSettings(BaseSettings):
    CRYPTO_PAY_TOKEN: str
    ACCEPTED_ASSETS: str

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env", env_file_encoding="utf8", extra="ignore"
    )


class YoomoneySettings(BaseSettings):
    YOOMONEY_CLIENT_ID: str
    YOOMONEY_REDIRECT_URL: str
    YOOMONEY_ACCOUNT_ID: str
    YOOMONEY_SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env", env_file_encoding="utf8", extra="ignore"
    )


class Settings(BaseSettings):
    MODE: str
    API_KEY_BOT: str
    ADMIN: int
    PRIVATE_CHANEL: int
    URL_CHANEL: str

    db_settings: DBSettings = DBSettings()
    redis_settings: RedisSettings = RedisSettings()
    crypto_settings: CryptoSettings = CryptoSettings()
    yoomoney_settings: YoomoneySettings = YoomoneySettings()

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env", env_file_encoding="utf8", extra="ignore"
    )


settings = Settings()
