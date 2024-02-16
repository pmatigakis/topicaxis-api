from topicaxisapi.database.models import Article
from topicaxisapi.mappers.base import Mapper
from topicaxisapi.models import Article as ArticleDomain
from topicaxisapi.models import (
    Category,
    Channel,
    ChannelPost,
    NamedEntity,
    NamedEntityType,
    Source,
    Tag,
)


class ArticleDatabaseToDomainMapper(Mapper[Article, ArticleDomain]):
    def map(self, item: Article) -> ArticleDomain:
        return ArticleDomain(
            id=item.id,
            title=item.title,
            url=item.url,
            description=item.description,
            image=item.image,
            summary=item.summary,
            source=Source(
                id=item.source["id"],
                name=item.source["name"],
                url=item.source["url"],
            ),
            categories=[
                Category(
                    id=category["id"],
                    name=category["name"],
                    taxonomy=category["taxonomy"],
                )
                for category in item.categories
            ],
            tags=[
                Tag(
                    id=tag["id"],
                    name=tag["name"],
                )
                for tag in item.tags
            ],
            channels=[
                Channel(
                    id=channel["id"],
                    name=channel["name"],
                    url=channel["url"],
                    posts=[
                        ChannelPost(
                            url=post["url"],
                            title=post["title"],
                            posted_at=post["posted_at"],
                        )
                        for post in channel["posts"]
                    ],
                )
                for channel in item.channels
            ],
            keywords=item.keywords,
            named_entities=[
                NamedEntity(
                    id=named_entity["id"],
                    value=named_entity["value"],
                    type=NamedEntityType(
                        id=named_entity["type"]["id"],
                        name=named_entity["type"]["name"],
                    ),
                )
                for named_entity in item.named_entities
            ],
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
