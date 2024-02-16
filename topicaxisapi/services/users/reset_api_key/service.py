from topicaxisapi.database.models import User
from topicaxisapi.repositories.users import UserRepository
from topicaxisapi.services.users.exceptions import UnknownUserError


class ResetApiKey:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def run(self, username) -> User:
        user = self._user_repository.get_by_username(username)
        if not user:
            raise UnknownUserError("user not fount")

        user.reset_api_key()
        self._user_repository.save(user)

        return user
