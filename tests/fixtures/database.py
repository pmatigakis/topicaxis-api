import pytest

from tests.factories.database import ArticleFactory, UserFactory


@pytest.fixture
def user(app_test_session):
    user_ = UserFactory()
    app_test_session.add(user_)
    app_test_session.commit()

    return user_


@pytest.fixture
def published_article(app_test_session):
    article = ArticleFactory()
    app_test_session.add(article)
    app_test_session.commit()

    return article
