from topicaxisapi.models import Categories
from topicaxisapi.repositories.base import Repository


class ListCategories:
    def __init__(self, category_repository: Repository):
        self._category_repository = category_repository

    def run(self) -> Categories:
        return Categories(categories=self._category_repository.list())
