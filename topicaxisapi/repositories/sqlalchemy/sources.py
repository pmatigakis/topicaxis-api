from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.session import Session

from topicaxisapi.database.models import Source
from topicaxisapi.mappers.database.sources import SourceDatabaseToDomainMapper
from topicaxisapi.models import Source as SourceDomain
from topicaxisapi.repositories.base import Repository
from topicaxisapi.repositories.filters import Filters


class SourceRepository(Repository[SourceDomain]):
    def __init__(self, session: Session):
        self._session = session

        self._mapper = SourceDatabaseToDomainMapper()

    def save(self, model: SourceDomain) -> SourceDomain:
        raise NotImplementedError()

    def delete(self, model: SourceDomain):
        raise NotImplementedError()

    def list(
        self,
        offset: int = 0,
        limit: int = 50,
        filters: Filters | None = None,
    ) -> list[SourceDomain]:
        query = (
            self._session.query(Source)
            .order_by(Source.name)
            .offset(offset)
            .limit(limit)
        )

        return [self._mapper.map(source) for source in query]

    def save_bulk(self, models: List[SourceDomain]):
        if not models:
            return

        sources_data = [source.dict() for source in models]
        stmt = insert(Source).values(sources_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                name=stmt.excluded.name,
                url=stmt.excluded.url,
            ),
        )
        self._session.execute(stmt)
