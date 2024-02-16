from topicaxisapi.database.models import Channel
from topicaxisapi.mappers.base import Mapper
from topicaxisapi.models import ChannelDetails


class ChannelDatabaseToDomainMapper(Mapper[Channel, ChannelDetails]):
    def map(self, item: Channel) -> ChannelDetails:
        return ChannelDetails(id=item.id, name=item.name, url=item.url)
