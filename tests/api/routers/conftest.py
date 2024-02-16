from datetime import datetime

import pytest
from faker import Faker

from topicaxisapi.database.models import (
    Article,
    Category,
    Channel,
    Source,
    Tag,
)


@pytest.fixture
def published_category(app_test_session):
    category = Category(
        id="category1",
        name="category 1",
        taxonomy={"id": "taxonomy1", "name": "topicaxis"},
    )
    app_test_session.add(category)
    app_test_session.commit()

    return category


@pytest.fixture
def published_channel(app_test_session):
    fake = Faker()

    channel = Channel(id=fake.word(), name=fake.word(), url=fake.url())
    app_test_session.add(channel)
    app_test_session.commit()

    return channel


@pytest.fixture
def published_source(app_test_session):
    fake = Faker()

    source = Source(id=fake.word(), name=fake.word(), url=fake.url())
    app_test_session.add(source)
    app_test_session.commit()

    return source


@pytest.fixture
def published_tag(app_test_session):
    fake = Faker()
    tag = Tag(id="tag1", name=fake.word())
    app_test_session.add(tag)
    app_test_session.commit()

    return tag


@pytest.fixture
def published_articles(
    topicaxis_api_settings,
    app_test_session,
    published_category,
    published_channel,
    published_source,
    published_tag,
):
    fake = Faker()

    categories_data = [
        {
            "id": published_category.id,
            "name": published_category.name,
            "taxonomy": published_category.taxonomy,
        }
    ]

    source_data = {
        "id": published_source.id,
        "name": published_source.name,
        "url": published_source.url,
    }

    tags_data = [{"id": published_tag.id, "name": published_tag.name}]

    channels_data = [
        {
            "id": published_channel.id,
            "name": published_channel.name,
            "url": published_channel.url,
            "posts": [
                {
                    "posted_at": fake.unix_time(),
                    "title": fake.sentence(),
                    "url": fake.url(),
                }
            ],
        }
    ]

    base_created_at = fake.unix_time()
    articles = [
        Article(
            **{
                "id": f"article{i}",
                "categories": categories_data,
                "created_at": datetime.fromtimestamp(base_created_at + i),
                "updated_at": datetime.fromtimestamp(base_created_at + i + 1),
                "source": source_data,
                "title": fake.sentence(),
                "url": fake.uri(),
                "tags": tags_data,
                "channels": channels_data,
                "description": fake.word(),
                "image": fake.url(),
                "summary": fake.sentence(),
                "keywords": [fake.word()],
                "named_entities": [
                    {
                        "id": f"namedentity{i}",
                        "value": fake.word(),
                        "type": {
                            "id": "namedentitytype1",
                            "name": "GEOPOLITICAL_ENTITY",
                        },
                    }
                ],
            }
        )
        for i in range(15)
    ]
    for article in articles:
        app_test_session.add(article)

    app_test_session.commit()

    return articles


@pytest.fixture
def published_articles_with_multiple_categories(
    mongodb_client, topicaxis_api_settings
):
    fake = Faker()

    source = {"id": fake.word(), "name": fake.word(), "url": fake.url()}

    articles = []
    i = 0
    for category_id in range(3):
        category_articles = []
        for _ in range(15):
            category_articles.append(
                {
                    "_id": str(i),
                    "page_id": i,
                    "categories": [
                        {
                            "id": f"category{category_id}",
                            "name": f"category {category_id}",
                        }
                    ],
                    "created_at": fake.unix_time(),
                    "id": f"article{i}",
                    "source": source,
                    "title": fake.sentence(),
                    "url": fake.uri(),
                    "tags": [{"id": "tag1", "name": fake.word()}],
                    "channels": [
                        {
                            "id": "feed1",
                            "name": fake.word(),
                            "url": fake.url(),
                            "posts": [
                                {
                                    "posted_at": fake.unix_time(),
                                    "title": fake.sentence(),
                                    "url": fake.url(),
                                }
                            ],
                        }
                    ],
                    "description": fake.word(),
                    "image": fake.url(),
                }
            )
            i += 1
        articles.extend(category_articles)

    db = mongodb_client[topicaxis_api_settings.mongodb_database]
    articles_collection = db[topicaxis_api_settings.articles_collection]
    articles_collection.insert_many(articles)

    return articles


@pytest.fixture
def published_channels(app_test_session, published_channel):
    fake = Faker()

    channels = [published_channel]
    for i in range(2):
        channel = Channel(id=fake.word(), name=fake.word(), url=fake.url())
        app_test_session.add(channel)
        channels.append(channel)

    app_test_session.commit()

    return channels


@pytest.fixture
def published_sources(app_test_session, published_source):
    fake = Faker()

    source = Source(id=fake.word(), name=fake.word(), url=fake.url())
    app_test_session.add(source)
    app_test_session.commit()

    return [published_source, source]


@pytest.fixture
def published_tags(app_test_session, published_tag):
    fake = Faker()

    tag = Tag(id=fake.word(), name=fake.word())
    app_test_session.add(tag)
    app_test_session.commit()

    return [published_tag, tag]
