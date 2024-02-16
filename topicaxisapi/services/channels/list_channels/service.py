from topicaxisapi.models import Channels
from topicaxisapi.repositories.base import Repository


class ListChannels:
    def __init__(self, channel_repository: Repository):
        self._channel_repository = channel_repository

    def run(self) -> Channels:
        return Channels(channels=self._channel_repository.list())
