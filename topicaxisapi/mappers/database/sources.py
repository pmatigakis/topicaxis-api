from topicaxisapi.database.models import Source
from topicaxisapi.mappers.base import Mapper
from topicaxisapi.models import Source as SourceDomain


class SourceDatabaseToDomainMapper(Mapper[Source, SourceDomain]):
    def map(self, item: Source) -> SourceDomain:
        return SourceDomain(id=item.id, name=item.name, url=item.url)
