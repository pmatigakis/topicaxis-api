from topicaxisapi.models import Articles
from topicaxisapi.repositories.base import Repository
from topicaxisapi.repositories.filters import ArticleFilters


class SearchArticles:
    def __init__(self, article_repository: Repository):
        self._article_repository = article_repository

    def run(
        self, filters: ArticleFilters, limit: int = 10, offset: int = 0
    ) -> Articles:
        articles = self._article_repository.list(
            offset=offset, limit=limit, filters=filters
        )

        return Articles(articles=articles)
