import logging
from os import getenv

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    title: str = "Topicaxis"
    version: str = "2.0"

    sentry_dsn: str | None = None
    sentry_log_level: int = logging.INFO
    sentry_event_level: int = logging.ERROR
    sentry_traces_sample_rate: float = 1.0

    openapi_url: str | None = None
    docs_url: str | None = None

    articles_per_page: int = 50

    sqlalchemy_url: str | None = None

    class Config:
        env_file = getenv("TOPICAXIS_API_CONFIG_FILE")
