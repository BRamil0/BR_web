import pydantic_settings

class Settings(pydantic_settings.BaseSettings):
    """Settings for the application."""
    host: str = "localhost"
    port: int = 8080
    DEBUG: bool = False
    BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: int = 0
    MONGODB_URI: str = "localhost:27017"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 180
    SECURE_COOKIES: bool = True
    default_theme_list: list = ["system", "light", "dark"]
    default_list_of_languages: list = ["eng", "ukr"]

    model_config = pydantic_settings.SettingsConfigDict(env_file=".config.env", env_file_encoding="utf-8")

settings: Settings = Settings()
