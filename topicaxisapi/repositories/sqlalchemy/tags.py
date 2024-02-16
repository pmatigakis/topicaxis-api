from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.session import Session

from topicaxisapi.database.models import Tag
from topicaxisapi.mappers.database.tags import TagDatabaseToDomainMapper
from topicaxisapi.models import Tag as TagDomain
from topicaxisapi.repositories.base import Repository
from topicaxisapi.repositories.filters import Filters


class TagRepository(Repository[TagDomain]):
    def __init__(self, session: Session):
        self._session = session

        self._mapper = TagDatabaseToDomainMapper()

    def save(self, model: TagDomain) -> TagDomain:
        raise NotImplementedError()

    def delete(self, model: TagDomain):
        raise NotImplementedError()

    def list(
        self,
        offset: int = 0,
        limit: int | None = None,
        filters: Filters | None = None,
    ) -> list[TagDomain]:
        query = self._session.query(Tag).order_by(Tag.name).offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return [self._mapper.map(tag) for tag in query]

    def save_bulk(self, models: List[TagDomain]):
        if not models:
            return

        tags_data = [tag.dict() for tag in models]
        stmt = insert(Tag).values(tags_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                name=stmt.excluded.name,
            ),
        )
        self._session.execute(stmt)
