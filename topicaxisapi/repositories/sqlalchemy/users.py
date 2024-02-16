from typing import List

from sqlalchemy.orm.session import Session

from topicaxisapi.database.models import User
from topicaxisapi.mappers.database.users import (
    UserDatabaseToDomainMapper,
    UserDomainToDatabaseMapper,
)
from topicaxisapi.models import User as UserDomain
from topicaxisapi.repositories.filters import Filters
from topicaxisapi.repositories.users import UserRepository


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self._session = session

        self._db_to_domain_mapper = UserDatabaseToDomainMapper()
        self._domain_to_db_mapper = UserDomainToDatabaseMapper()

    def list(
        self,
        offset: int = 0,
        limit: int = 10,
        filters: Filters | None = None,
    ) -> list[UserDomain]:
        raise NotImplementedError()

    def save_bulk(self, models: List[UserDomain]):
        raise NotImplementedError()

    def save(self, model: UserDomain) -> UserDomain:
        user = self._domain_to_db_mapper.map(model)
        self._session.merge(user)
        self._session.flush()
        model.id = user.id

        return model

    def get_by_username(self, username: str) -> UserDomain | None:
        user = (
            self._session.query(User)
            .filter(User.username == username)
            .one_or_none()
        )
        if not user:
            return None

        return self._db_to_domain_mapper.map(user)

    def delete(self, model: UserDomain):
        self._session.query(User).filter(User.id == model.id).delete()
