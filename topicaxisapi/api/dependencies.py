from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from topicaxisapi.configuration import Settings
from topicaxisapi.database import postgres
from topicaxisapi.database.models import User

apikey_scheme = APIKeyHeader(name="apikey")


def get_settings() -> Settings:
    return Settings()


def get_engine(settings: Settings = Depends(get_settings)) -> Engine:
    if not postgres.engine:
        postgres.engine = create_engine(settings.sqlalchemy_url)

    return postgres.engine


def get_session(engine: Engine = Depends(get_engine)) -> Session:
    if not postgres.Session:
        postgres.Session = sessionmaker(engine)

    session = postgres.Session()
    try:
        yield session
    finally:
        session.close()


def get_api_key(
    api_key: Annotated[str, Security(apikey_scheme)],
    session: Session = Depends(get_session),
):
    user = session.query(User).filter(User.api_key == api_key).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid api key",
        )

    return api_key
