import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from topicaxisapi.api import dependencies
from topicaxisapi.models import Tags
from topicaxisapi.repositories.sqlalchemy.tags import TagRepository
from topicaxisapi.services.tags.list_tags.service import ListTags

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(dependencies.get_api_key)])


@router.get(
    "/v2/tags",
    tags=["tags"],
    summary="Get the tags",
    description="Get the available tags",
)
async def get_tags(
    session: Session = Depends(dependencies.get_session),
) -> Tags:
    repository = TagRepository(session)
    list_tags = ListTags(repository)

    return list_tags.run()
