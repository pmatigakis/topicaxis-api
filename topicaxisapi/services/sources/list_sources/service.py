from logging import getLogger

from topicaxisapi.models import Sources
from topicaxisapi.repositories.base import Repository

logger = getLogger(__name__)


class ListSources:
    def __init__(self, source_repository: Repository):
        self._source_repository = source_repository

    def run(self, offset: int = 0, limit: int = 50) -> Sources:
        return Sources(sources=self._source_repository.list(offset, limit))
