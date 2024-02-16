import json
from datetime import datetime
from itertools import islice

from topicaxisapi.models import Article, Category, ChannelDetails, Source, Tag
from topicaxisapi.repositories.base import Repository
from topicaxisapi.services.articles.load_articles.models import (
    LoadArticlesResult,
)


class LoadArticles:
    def __init__(
        self,
        article_repository: Repository,
        category_repository: Repository,
        channel_repository: Repository,
        tag_repository: Repository,
        source_repository: Repository,
    ):
        self._article_repository = article_repository
        self._category_repository = category_repository
        self._channel_repository = channel_repository
        self._source_repository = source_repository
        self._tag_repository = tag_repository

    def run(self, articles_file: str) -> LoadArticlesResult:
        categories = {}
        channels = {}
        tags = {}
        line_count = 0
        with open(articles_file) as f:
            while True:
                lines = list(islice(f, 10))
                if not lines:
                    break

                articles = []
                sources = {}
                articles_data = [json.loads(line) for line in lines]
                for article_data in articles_data:
                    line_count += 1
                    if "page_id" in article_data:
                        article_data.pop("page_id")

                    article_data["created_at"] = datetime.fromtimestamp(
                        article_data.pop("created_at")
                    )
                    articles.append(Article(**article_data))

                    for category_data in article_data["categories"]:
                        if category_data["id"] not in categories:
                            categories[category_data["id"]] = Category(
                                **category_data
                            )

                    for channel_data in article_data["channels"]:
                        if channel_data["id"] not in channels:
                            channels[channel_data["id"]] = ChannelDetails(
                                id=channel_data["id"],
                                name=channel_data["name"],
                                url=channel_data["url"],
                            )

                    for tag_data in article_data["tags"]:
                        if tag_data["id"] not in tags:
                            tags[tag_data["id"]] = Tag(**tag_data)

                    if article_data["source"]["id"] not in sources:
                        sources[article_data["source"]["id"]] = Source(
                            **article_data["source"]
                        )

                self._article_repository.save_bulk(articles)
                self._source_repository.save_bulk(list(sources.values()))

        self._category_repository.save_bulk(list(categories.values()))
        self._channel_repository.save_bulk(list(channels.values()))
        self._tag_repository.save_bulk(list(tags.values()))

        return LoadArticlesResult(lines_processed=line_count)
