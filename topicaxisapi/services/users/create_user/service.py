from topicaxisapi.models import User
from topicaxisapi.repositories.users import UserRepository


class CreateUser:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def run(self, username) -> User:
        user = User(username=username)
        user.reset_api_key()
        user = self._user_repository.save(user)

        return user
