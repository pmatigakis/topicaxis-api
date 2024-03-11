import logging

import sentry_sdk
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from topicaxisapi.api.exceptions import ArticleSearchError
from topicaxisapi.api.routers import (
    articles,
    categories,
    channels,
    sources,
    tags,
)
from topicaxisapi.configuration import Settings
from topicaxisapi.database import postgres

logger = logging.getLogger(__name__)


def _initialize_sentry(settings: Settings):
    if settings.sentry_dsn is None:
        return

    sentry_logging = LoggingIntegration(
        level=settings.sentry_log_level,
        event_level=settings.sentry_event_level,
    )

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[sentry_logging],
        traces_sample_rate=settings.sentry_traces_sample_rate,
    )


def _add_routers(app: FastAPI):
    app.include_router(articles.router)
    app.include_router(categories.router)
    app.include_router(channels.router)
    app.include_router(tags.router)
    app.include_router(sources.router)


def _initialize_error_handlers(app):
    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": "Invalid request."}),
        )

    @app.exception_handler(ArticleSearchError)
    def article_search_error_handler(
        request: Request, exc: ArticleSearchError
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(
                {"detail": "failed to execute article search"}
            ),
        )


def _setup_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    settings = Settings()

    _initialize_sentry(settings)

    app = FastAPI(
        title=settings.title,
        version=settings.version,
        openapi_url=settings.openapi_url,
        docs_url=settings.docs_url,
        redoc_url=None,
    )

    _setup_middlewares(app)
    _add_routers(app)
    _initialize_error_handlers(app)

    @app.on_event("shutdown")
    def shutdown_db_client():
        if postgres.Session:
            postgres.Session.close_all()
            postgres.Session = None

        if postgres.engine:
            postgres.engine.dispose()
            postgres.engine = None

    return app
