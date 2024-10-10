import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Settings for the application."""
    HOST: str = "localhost"
    PORT: int = 8080
    DEBUG: bool = False

    model_config = pydantic_settings.SettingsConfigDict(env_file=".config.env")


settings = Settings()
