import json
import os
import typing
import enum

import toml
import yaml
import pathlib
import pydantic_settings
import dotenv

from src.logger.logger import logger

class LoadTypeFile(enum.Enum):
    yaml = "_load_yaml"
    json = "_load_json"
    toml = "_load_toml"


class Settings(pydantic_settings.BaseSettings):
    """Settings for the application."""

    DEBUG: bool = False
    DEBUG_DATABASE: bool = False

    BOT_TOKEN: str = None
    TELEGRAM_CHAT_ID: int = None
    MONGODB_URI: str = None
    SECRET_KEY: str = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 180
    SECURE_COOKIES: bool = True

    host: str = "localhost"
    port: int = 8080
    default_theme_list: typing.List[str] = ["system", "light", "dark"]
    default_list_of_languages: typing.List[str] = ["eng", "ukr"]
    default_theme: str = "system"
    default_language: str = "eng"
    log_dir: str = "/tmp/logs/"
    is_log_record: bool = False

    class Config:
        env_file = ".config.env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs: typing.Any):
        super().__init__(**kwargs)
        self.load_env_file()

    def check_for_none_values(self):
        for field, value in self.__dict__.items():
            if value is None or value == "":
                raise ValueError(f"Field '{field}' cannot be None or empty.")

    def load_env_file(self):
        env_file = self.Config.env_file
        if os.path.exists(env_file):
            logger.opt(colors=True).info(f"<blue>Settings</blue> | <c>Load config from env-file: <b>{env_file}</b></c>")
            self.load_from_env()
        else:
            logger.opt(colors=True).info(f"<blue>Settings</blue> | <c>Env file not found, checking environment variables...</c>")
            dotenv.load_dotenv()

    def load_from_env(self):
        for field in self.__annotations__:
            env_value = os.getenv(field.upper())
            if env_value is not None:
                setattr(self, field, env_value)
            elif not hasattr(self, field):
                raise ValueError(f"Field '{field}' is missing in the environment variables.")

    def load_config_file(self):
        config_files = [
            ("config.yaml", "yaml"),
            ("config.json", "json"),
            ("config.toml", "toml")
        ]

        for file_name, file_type in config_files:
            if pathlib.Path(file_name).is_file():
                logger.opt(colors=True).info(f"<blue>Settings</blue> | <c>Load config file: <b>{file_name}</b></c>")
                self.load_from_file(file_name, file_type)
                break
        else:
            logger.opt(colors=True).warning("<blue>Settings</blue> | <c>Config file not found</c> <y>(create the file “config.json/yaml/toml” in the project root)</y>")

    def load_from_file(self, config_file: str, file_type: str = "yaml"):
        try:
            handler = getattr(self, LoadTypeFile[file_type].value)
            return handler(config_file)
        except KeyError:
            logger.opt(colors=True).critical(f"<blue>Settings</blue> | <c>Unsupported file type: <b>{file_type}</b></c>")
            raise ValueError(f"Unsupported file type: {file_type}")

    def _load_config(self, data: dict[str, str | int | typing.List[str]]):
        for key, value in data.items():
            setattr(self, key, value)

    def _load_yaml(self, file_path: str):
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        self._load_config(data)

    def _load_json(self, file_path: str):
        with open(file_path, "r") as f:
            data = json.load(f)
        self._load_config(data)

    def _load_toml(self, file_path: str):
        data = toml.load(file_path)
        self._load_config(data)

try:
    settings = Settings()
    settings.load_config_file()
    settings.check_for_none_values()
except ValueError as e:
    logger.opt(colors=True).critical(f"<blue>Settings</blue> | <c>Load config file error</c> <y>{e}</y>")
    raise ValueError(f"Load config file error: {e}")
