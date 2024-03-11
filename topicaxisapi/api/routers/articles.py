import logging
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session

from topicaxisapi.api import dependencies
from topicaxisapi.api.exceptions import ArticleSearchError
from topicaxisapi.models import Articles
from topicaxisapi.repositories.filters import ArticleFilters
from topicaxisapi.repositories.sqlalchemy.articles import ArticleRepository
from topicaxisapi.services.articles.search_articles.service import (
    SearchArticles,
)

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(dependencies.get_api_key)])


@router.get(
    "/v2/articles",
    tags=["articles"],
    summary="Get articles",
    description="Get articles that have been published",
)
def search_articles(
    query: str
    | None = Query(
        default=None,
        title="Query string",
        description="The query to execute",
        min_length=1,
        max_length=120,
    ),
    categories: str
    | None = Query(
        default=None,
        title="Categories",
        description="The required article categories",
        min_length=1,
        max_length=200,
        regex=r"^[\w\d]+(,[\w\d]+)*$",
    ),
    source: str
    | None = Query(
        default=None,
        title="Source",
        description="The required article source",
        min_length=1,
        max_length=200,
        regex=r"^[\w\d]+$",
    ),
    tags: str
    | None = Query(
        default=None,
        title="Tags",
        description="The required article tags",
        min_length=1,
        max_length=200,
        regex=r"^[\w\d]+(,[\w\d]+)*$",
    ),
    channels: str
    | None = Query(
        default=None,
        title="Channels",
        description="The required article channels",
        min_length=1,
        max_length=200,
        regex=r"^[\w\d]+(,[\w\d]+)*$",
    ),
    from_date: datetime
    | None = Query(
        default=None,
        title="From date",
        description="Return articles after the date",
    ),
    to_date: datetime
    | None = Query(
        default=None,
        title="To date",
        description="Return articles to the date",
    ),
    limit: int
    | None = Query(
        default=20,
        title="Article limit",
        description="The number of articles to return",
        ge=1,
        le=20,
    ),
    offset: int
    | None = Query(
        default=0,
        title="Result offset",
        description="The offset of the results",
        ge=0,
    ),
    session: Session = Depends(dependencies.get_session),
) -> Articles:
    if categories is not None:
        categories = categories.split(",")

    if tags is not None:
        tags = tags.split(",")

    if channels is not None:
        channels = channels.split(",")

    article_repository = ArticleRepository(session)
    search_articles_ = SearchArticles(article_repository)
    try:
        return search_articles_.run(
            filters=ArticleFilters(
                text=query,
                categories=categories,
                source=source,
                tags=tags,
                channels=channels,
                from_date=from_date,
                to_date=to_date,
            ),
            offset=offset,
            limit=limit,
        )
    except Exception as e:
        logger.exception("failed to execute article search query")

        raise ArticleSearchError() from e
