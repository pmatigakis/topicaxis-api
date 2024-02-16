from topicaxisapi.database.models import User
from topicaxisapi.mappers.base import Mapper
from topicaxisapi.models import User as UserDomain


class UserDatabaseToDomainMapper(Mapper[User, UserDomain]):
    def map(self, item: User) -> UserDomain:
        return UserDomain(
            id=item.id, username=item.username, api_key=item.api_key
        )


class UserDomainToDatabaseMapper(Mapper[UserDomain, User]):
    def map(self, item: UserDomain) -> User:
        return User(id=item.id, username=item.username, api_key=item.api_key)
