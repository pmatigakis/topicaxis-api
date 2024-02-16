from abc import ABC

from topicaxisapi.models import User as UserDomain
from topicaxisapi.repositories.base import Repository


class UserRepository(Repository[UserDomain], ABC):
    def get_by_username(self, username: str) -> UserDomain | None:
        ...
