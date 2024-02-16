import pytest
from faker import Faker


@pytest.fixture
def article_data() -> dict:
    fake = Faker()

    created_at = fake.unix_time()
    posted_at = created_at - 10
    title = fake.sentence()
    url = fake.uri()

    return dict(
        id="article1",
        page_id=1,
        categories=[
            {
                "id": fake.word(),
                "name": fake.word(),
                "taxonomy": {"id": fake.word(), "name": fake.word()},
            }
        ],
        created_at=created_at,
        source={"id": "source2", "name": fake.word(), "url": fake.url()},
        title=title,
        url=url,
        tags=[{"id": "tag1", "name": fake.word()}],
        channels=[
            {
                "id": "channel1",
                "name": fake.word(),
                "url": fake.url(),
                "posts": [
                    {"posted_at": posted_at, "title": title, "url": url}
                ],
            }
        ],
        description=fake.word(),
        image=fake.url(),
        summary="hello world",
        keywords=[fake.word()],
        named_entities=[
            {
                "id": "namedentity1",
                "value": fake.word(),
                "type": {
                    "id": "namedentitytype1",
                    "name": "GEOPOLITICAL_ENTITY",
                },
            }
        ],
    )
