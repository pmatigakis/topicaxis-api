import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from topicaxisapi.api import dependencies
from topicaxisapi.models import Categories
from topicaxisapi.repositories.sqlalchemy.categories import CategoryRepository
from topicaxisapi.services.categories.list_categories.service import (
    ListCategories,
)

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(dependencies.get_api_key)])


@router.get(
    "/v2/categories",
    tags=["categories"],
    summary="Get categories",
    description="Get the available categories",
)
def get_categories(
    session: Session = Depends(dependencies.get_session),
) -> Categories:
    logger.info("Retrieving available categories")
    category_repository = CategoryRepository(session)
    list_categories = ListCategories(category_repository)

    return list_categories.run()
