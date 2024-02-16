from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.session import Session

from topicaxisapi.database.models import Category
from topicaxisapi.mappers.database.categories import (
    CategoryDatabaseToDomainMapper,
)
from topicaxisapi.models import Category as CategoryDomain
from topicaxisapi.repositories.base import Repository
from topicaxisapi.repositories.filters import Filters


class CategoryRepository(Repository[CategoryDomain]):
    def __init__(self, session: Session):
        self._session = session

        self._mapper = CategoryDatabaseToDomainMapper()

    def save(self, model: CategoryDomain) -> CategoryDomain:
        raise NotImplementedError()

    def delete(self, model: CategoryDomain):
        raise NotImplementedError()

    def list(
        self,
        offset: int = 0,
        limit: int | None = None,
        filters: Filters | None = None,
    ) -> list[CategoryDomain]:
        query = (
            self._session.query(Category)
            .order_by(Category.name)
            .offset(offset)
        )

        if limit is not None:
            query = query.limit(limit)

        return [self._mapper.map(category) for category in query]

    def save_bulk(self, models: List[CategoryDomain]):
        if not models:
            return

        category_data = [article.dict() for article in models]
        stmt = insert(Category).values(list(category_data))
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                name=stmt.excluded.name,
                taxonomy=stmt.excluded.taxonomy,
            ),
        )
        self._session.execute(stmt)
