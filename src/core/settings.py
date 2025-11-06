from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env", env_file_encoding="utf8", extra="ignore"
    )


class WebhookSettings(EnvBaseSettings):
    WEBHOOK_BASE_URL: str
    WEBHOOK_SECRET: str
    WEBHOOK_HOST: str
    WEBHOOK_PORT: int
    WEBHOOK_PATH: str

    @property
    def webhook_url(self) -> str:
        return f"{self.WEBHOOK_BASE_URL}{self.WEBHOOK_PATH}"


class BotSettings(WebhookSettings):
    API_KEY_BOT: str
    ADMIN: int
    PRIVATE_CHANEL: int
    URL_CHANEL: str


class PgSettings(EnvBaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: SecretStr
    DB_NAME: str

    @property
    def pgdb_url(self):
        return (
            f"postgresql+asyncpg:"
            f"//{self.DB_USER}:"
            f"{self.DB_PASS.get_secret_value()}"
            f"@{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


class RedisSettings(EnvBaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


class PaymentSettings(EnvBaseSettings):
    CRYPTO_PAY_TOKEN: str
    ACCEPTED_ASSETS: str

    YOOMONEY_CLIENT_ID: str
    YOOMONEY_REDIRECT_URL: str
    YOOMONEY_ACCOUNT_ID: str
    YOOMONEY_SECRET_KEY: str


class Settings(BotSettings, PgSettings, RedisSettings, PaymentSettings):
    MODE: str


settings = Settings()
