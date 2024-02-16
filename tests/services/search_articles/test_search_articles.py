from datetime import timedelta

from topicaxisapi.models import Article, Articles
from topicaxisapi.repositories.filters import ArticleFilters
from topicaxisapi.services.articles.search_articles.service import (
    SearchArticles,
)


def test_search_articles_when_there_are_no_pages(article_repository):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=None,
            source=None,
            tags=None,
            channels=None,
            from_date=None,
            to_date=None,
        )
    )

    assert article_query_result == Articles(articles=[])


def test_search_article(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=None,
            source=None,
            tags=None,
            channels=None,
            from_date=None,
            to_date=None,
        )
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_text(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=published_article.title,
            categories=None,
            source=None,
            tags=None,
            channels=None,
            from_date=None,
            to_date=None,
        )
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_categories(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=[published_article.categories[0]["id"]],
            source=None,
            tags=None,
            channels=None,
            from_date=None,
            to_date=None,
        )
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_source(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=None,
            source=published_article.source["id"],
            tags=None,
            channels=None,
            from_date=None,
            to_date=None,
        )
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_tags(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=None,
            source=None,
            tags=[published_article.tags[0]["id"]],
            channels=None,
            from_date=None,
            to_date=None,
        )
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_channels(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=None,
            source=None,
            tags=None,
            channels=[published_article.channels[0]["id"]],
            from_date=None,
            to_date=None,
        )
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_from_date(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=None,
            source=None,
            tags=None,
            channels=None,
            from_date=published_article.created_at,
            to_date=None,
        )
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_to_date(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=None,
            source=None,
            tags=None,
            channels=None,
            from_date=None,
            to_date=published_article.created_at + timedelta(seconds=1),
        )
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_date_range(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=None,
            source=None,
            tags=None,
            channels=None,
            from_date=published_article.created_at - timedelta(seconds=1),
            to_date=published_article.created_at + timedelta(seconds=1),
        )
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_text_and_filters(
    article_repository, published_article
):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=published_article.title,
            categories=[published_article.categories[0]["id"]],
            source=None,
            tags=None,
            channels=None,
            from_date=None,
            to_date=None,
        )
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_limit(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=None,
            source=None,
            tags=None,
            channels=None,
            from_date=None,
            to_date=None,
        ),
        limit=5,
    )

    assert article_query_result == Articles(
        articles=[
            Article(
                id=published_article.id,
                title=published_article.title,
                url=published_article.url,
                description=published_article.description,
                image=published_article.image,
                summary=published_article.summary,
                source=published_article.source,
                categories=published_article.categories,
                tags=published_article.tags,
                channels=published_article.channels,
                keywords=published_article.keywords,
                named_entities=published_article.named_entities,
                created_at=published_article.created_at,
                updated_at=published_article.updated_at,
            )
        ]
    )


def test_search_article_with_offset(article_repository, published_article):
    article_service = SearchArticles(article_repository)

    article_query_result = article_service.run(
        ArticleFilters(
            text=None,
            categories=None,
            source=None,
            tags=None,
            channels=None,
            from_date=None,
            to_date=None,
        ),
        offset=3,
    )

    assert article_query_result == Articles(articles=[])
