import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Settings for the application."""
    HOST: str = "localhost"
    PORT: int = 8080
    DEBUG: bool = False
    BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: int = 0
    MONGODB_URI: str = "localhost:27017"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 180
    SECURE_COOKIES: bool = True

    model_config = pydantic_settings.SettingsConfigDict(env_file=".config.env")


settings: Settings = Settings()
