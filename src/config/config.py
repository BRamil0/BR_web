import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Settings for the application."""
    HOST: str = "localhost"
    PORT: int = 8080
    DEBUG: bool = False
    BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: int = 0
    MONGODB_URI: str = "localhost:27017"

    model_config = pydantic_settings.SettingsConfigDict(env_file=".config.env")


settings: Settings = Settings()
