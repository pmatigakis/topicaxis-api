from topicaxisapi.models import Tags
from topicaxisapi.repositories.base import Repository


class ListTags:
    def __init__(self, tag_repository: Repository):
        self._tag_repository = tag_repository

    def run(self) -> Tags:
        return Tags(tags=self._tag_repository.list())
