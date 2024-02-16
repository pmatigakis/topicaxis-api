from topicaxisapi.repositories.users import UserRepository
from topicaxisapi.services.users.exceptions import UnknownUserError


class GetUserApiKey:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def run(self, username) -> str:
        user = self._user_repository.get_by_username(username)
        if not user:
            raise UnknownUserError("user not fount")

        return user.api_key
