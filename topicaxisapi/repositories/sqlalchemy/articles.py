from datetime import datetime
from typing import List

from sqlalchemy import and_, desc, or_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import func

from topicaxisapi.database.models import Article
from topicaxisapi.mappers.database.articles import (
    ArticleDatabaseToDomainMapper,
)
from topicaxisapi.models import Article as ArticleDomain
from topicaxisapi.repositories.base import Repository
from topicaxisapi.repositories.filters import ArticleFilters


class ArticleRepository(Repository[ArticleDomain]):
    def __init__(self, session: Session):
        self._session = session

        self._mapper = ArticleDatabaseToDomainMapper()

    def save(self, model: ArticleDomain) -> ArticleDomain:
        raise NotImplementedError()

    def delete(self, model: ArticleDomain):
        raise NotImplementedError()

    def list(
        self,
        offset: int = 0,
        limit: int = 10,
        filters: ArticleFilters | None = None,
    ) -> list[ArticleDomain]:
        query = self._session.query(Article)
        if not filters.text:
            query = query.order_by(desc(Article.updated_at), desc(Article.id))
        else:
            query_text = func.plainto_tsquery(filters.text)
            query = query.filter(
                or_(
                    func.to_tsvector("english", Article.title).op("@@")(
                        query_text
                    ),
                    func.to_tsvector("english", Article.summary).op("@@")(
                        query_text
                    ),
                )
            )

        if filters.source:
            query = query.filter(Article.source["id"].astext == filters.source)

        if filters.categories:
            category_filters = [
                Article.categories.contains([{"id": category_id}])
                for category_id in filters.categories
            ]
            query = query.filter(and_(*category_filters))

        if filters.channels:
            channel_filters = [
                Article.channels.contains([{"id": channel_id}])
                for channel_id in filters.channels
            ]
            query = query.filter(and_(*channel_filters))

        if filters.tags:
            tag_filters = [
                Article.tags.contains([{"id": tag_id}])
                for tag_id in filters.tags
            ]
            query = query.filter(and_(*tag_filters))

        if filters.from_date:
            query = query.filter(Article.created_at >= filters.from_date)

        if filters.to_date:
            query = query.filter(Article.created_at < filters.to_date)

        articles = list(query.offset(offset).limit(limit))

        return [self._mapper.map(article) for article in articles]

    def save_bulk(self, models: List[ArticleDomain]):
        if not models:
            return

        updated_at = datetime.now()
        articles_data = [article.dict() for article in models]
        for article_data in articles_data:
            article_data["created_at"] = datetime.fromtimestamp(
                article_data["created_at"]
            )
            article_data["updated_at"] = updated_at

        stmt = insert(Article).values(articles_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                categories=stmt.excluded.categories,
                source=stmt.excluded.source,
                title=stmt.excluded.title,
                tags=stmt.excluded.tags,
                channels=stmt.excluded.channels,
                description=stmt.excluded.description,
                image=stmt.excluded.image,
                summary=stmt.excluded.summary,
                keywords=stmt.excluded.keywords,
                named_entities=stmt.excluded.named_entities,
                updated_at=stmt.excluded.updated_at,
            ),
        )
        self._session.execute(stmt)
