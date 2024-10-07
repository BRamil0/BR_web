import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEBUG: bool = False

    model_config = pydantic_settings.SettingsConfigDict(env_file=".config.env")


settings = Settings()
