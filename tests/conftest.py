import asyncio
from os import environ
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from tests import database
from topicaxisapi.api.application import create_app
from topicaxisapi.api.dependencies import get_settings
from topicaxisapi.configuration import Settings
from topicaxisapi.database import postgres
from topicaxisapi.database.models import Base
from topicaxisapi.repositories.sqlalchemy.articles import ArticleRepository


@pytest.fixture()
def configuration() -> dict:
    config = dict(
        articles_per_page="10",
        sqlalchemy_url="postgresql+psycopg2://topicaxis:topicaxis@localhost:5432/topicaxis_api_tests",  # noqa
    )
    with patch.dict(environ, config, clear=True):
        yield config


@pytest.fixture
def topicaxis_api_settings(configuration) -> Settings:
    return Settings()


@pytest.fixture
def app_test_engine(topicaxis_api_settings):
    engine = create_engine(topicaxis_api_settings.sqlalchemy_url)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def app_test_sessionmaker(app_test_engine):
    Session = sessionmaker(app_test_engine)
    yield Session
    Session.close_all()


@pytest.fixture
def app_test_session(app_test_sessionmaker) -> Session:
    session = app_test_sessionmaker()
    database.session = session
    try:
        yield session
    finally:
        session.close()

    database.session = None


@pytest.fixture
def topicaxis_api_app(topicaxis_api_settings, app_test_engine):
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: topicaxis_api_settings

    yield app

    if postgres.Session:
        postgres.Session.close_all()
        postgres.Session = None

    if postgres.engine:
        postgres.engine.dispose()
        postgres.engine = None


@pytest.fixture
def topicaxis_api_client(topicaxis_api_app):
    return TestClient(topicaxis_api_app)


@pytest.fixture
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def article_repository(app_test_session):
    return ArticleRepository(app_test_session)


from tests.fixtures.database import *  # noqa
from tests.fixtures.json import *  # noqa
