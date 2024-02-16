from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.session import Session

from topicaxisapi.database.models import Channel
from topicaxisapi.mappers.database.channels import (
    ChannelDatabaseToDomainMapper,
)
from topicaxisapi.models import ChannelDetails
from topicaxisapi.repositories.base import Repository
from topicaxisapi.repositories.filters import Filters


class ChannelRepository(Repository[ChannelDetails]):
    def __init__(self, session: Session):
        self._session = session

        self._mapper = ChannelDatabaseToDomainMapper()

    def save(self, model: ChannelDetails) -> ChannelDetails:
        raise NotImplementedError()

    def delete(self, model: ChannelDetails):
        raise NotImplementedError()

    def list(
        self,
        offset: int = 0,
        limit: int | None = None,
        filters: Filters | None = None,
    ) -> list[ChannelDetails]:
        query = (
            self._session.query(Channel).order_by(Channel.name).offset(offset)
        )

        if limit is not None:
            query = query.limit(limit)

        return [self._mapper.map(channel) for channel in query]

    def save_bulk(self, models: List[ChannelDetails]):
        if not models:
            return

        channels_data = [channel.dict() for channel in models]
        stmt = insert(Channel).values(channels_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                name=stmt.excluded.name,
                url=stmt.excluded.url,
            ),
        )
        self._session.execute(stmt)
