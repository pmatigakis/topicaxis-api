from topicaxisapi.repositories.users import UserRepository
from topicaxisapi.services.users.exceptions import UnknownUserError


class DeleteUser:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def run(self, username):
        user = self._user_repository.get_by_username(username)
        if not user:
            raise UnknownUserError("user not fount")

        self._user_repository.delete(user)
