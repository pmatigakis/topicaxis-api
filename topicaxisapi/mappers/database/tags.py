from topicaxisapi.database.models import Tag
from topicaxisapi.mappers.base import Mapper
from topicaxisapi.models import Tag as TagDomain


class TagDatabaseToDomainMapper(Mapper[Tag, TagDomain]):
    def map(self, item: Tag) -> TagDomain:
        return TagDomain(id=item.id, name=item.name)
