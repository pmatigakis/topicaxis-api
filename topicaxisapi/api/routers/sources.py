import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session

from topicaxisapi.api import dependencies
from topicaxisapi.models import Sources
from topicaxisapi.repositories.sqlalchemy.sources import SourceRepository
from topicaxisapi.services.sources.list_sources.service import ListSources

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(dependencies.get_api_key)])


@router.get(
    "/v2/sources",
    tags=["sources"],
    summary="Get the sources",
    description="Get the available sources",
)
def get_sources(
    session: Session = Depends(dependencies.get_session),
    offset: int
    | None = Query(
        default=0,
        title="Sources offset",
        description="The offset of the sources results",
        ge=0,
    ),
    limit: int
    | None = Query(
        default=50,
        title="Sources limit",
        description="The number of sources to return",
        ge=1,
        le=100,
    ),
) -> Sources:
    source_repository = SourceRepository(session)
    list_sources = ListSources(source_repository)

    return list_sources.run(offset=offset, limit=limit)
