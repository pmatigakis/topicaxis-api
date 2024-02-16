from datetime import timedelta
from urllib.parse import urljoin

from factory import Faker, LazyAttribute, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from tests import database
from topicaxisapi.database.models import Article, User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_factory = lambda: database.session  # noqa: E731

    username = Sequence(lambda n: "user%d" % n)
    api_key = Sequence(lambda n: "apikey%d" % n)


class ArticleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Article
        sqlalchemy_session = None
        sqlalchemy_session_factory = lambda: database.session  # noqa: E731

    id = Sequence(lambda n: "article%d" % n)
    categories = [
        {
            "id": "category1",
            "name": "nategory1name",
            "taxonomy": {"id": "taxonomy1", "name": "taxonomy1.name"},
        }
    ]
    created_at = Faker("date_time_this_month")
    updated_at = LazyAttribute(lambda o: o.created_at + timedelta(seconds=1))
    source = {
        "id": "source1",
        "name": "source1name",
        "url": "https://source1.com",
    }
    title = Sequence(lambda n: "article %d title" % n)
    url = LazyAttribute(lambda o: urljoin(o.source["url"], o.id))
    tags = [{"id": "tag1", "name": "tag1name"}]
    channels = LazyAttribute(
        lambda o: [
            {
                "id": "channel1",
                "name": "channel1name",
                "url": "https://channel1.com",
                "posts": [
                    {
                        "posted_at": o.created_at.timestamp(),
                        "title": o.title,
                        "url": o.url,
                    }
                ],
            }
        ]
    )
    description = Sequence(lambda n: "article %d description" % n)
    image = LazyAttribute(lambda o: urljoin(o.source["url"], f"{o.id}.png"))
    summary = Sequence(lambda n: "article %d summary" % n)
    keywords = ["keyword1"]
    named_entities = [
        {
            "id": "namedentity1",
            "value": "namedentity1value",
            "type": {
                "id": "namedentitytype1",
                "name": "GEOPOLITICAL_ENTITY",
            },
        }
    ]
