from datetime import timedelta


def test_search_articles_when_there_are_no_articles(
    topicaxis_api_client, user
):
    response = topicaxis_api_client.get(
        "/v2/articles", headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {"articles": []}


def test_search_articles(topicaxis_api_client, user, published_article):
    expected_response = {
        key: getattr(published_article, key)
        for key in [
            "categories",
            "channels",
            "created_at",
            "updated_at",
            "description",
            "id",
            "image",
            "source",
            "tags",
            "title",
            "url",
            "summary",
            "keywords",
            "named_entities",
        ]
    }
    expected_response["created_at"] = expected_response[
        "created_at"
    ].timestamp()
    expected_response["updated_at"] = expected_response[
        "updated_at"
    ].timestamp()

    response = topicaxis_api_client.get(
        "/v2/articles", headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {"articles": [expected_response]}


def test_search_articles_with_offset(
    topicaxis_api_client, user, published_articles
):
    expected_response = [
        {
            key: getattr(article, key)
            for key in [
                "categories",
                "channels",
                "created_at",
                "updated_at",
                "description",
                "id",
                "image",
                "source",
                "tags",
                "title",
                "url",
                "summary",
                "keywords",
                "named_entities",
            ]
        }
        for article in (
            sorted(
                published_articles,
                key=lambda article: (article.updated_at, article.id),
                reverse=True,
            )[5:]
        )
    ]
    for item in expected_response:
        item["created_at"] = item["created_at"].timestamp()
        item["updated_at"] = item["updated_at"].timestamp()

    response = topicaxis_api_client.get(
        "/v2/articles", params={"offset": 5}, headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {"articles": expected_response}


def test_search_articles_with_limit(
    topicaxis_api_client, user, published_articles
):
    expected_response = [
        {
            key: getattr(article, key)
            for key in [
                "categories",
                "channels",
                "created_at",
                "updated_at",
                "description",
                "id",
                "image",
                "source",
                "tags",
                "title",
                "url",
                "summary",
                "keywords",
                "named_entities",
            ]
        }
        for article in (
            sorted(
                published_articles,
                key=lambda article: (article.updated_at, article.id),
                reverse=True,
            )[:3]
        )
    ]
    for item in expected_response:
        item["created_at"] = item["created_at"].timestamp()
        item["updated_at"] = item["updated_at"].timestamp()

    response = topicaxis_api_client.get(
        "/v2/articles", params={"limit": 3}, headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {"articles": expected_response}


def test_search_articles_with_query(
    topicaxis_api_client, user, published_article
):
    expected_response = {
        key: getattr(published_article, key)
        for key in [
            "categories",
            "channels",
            "created_at",
            "updated_at",
            "description",
            "id",
            "image",
            "source",
            "tags",
            "title",
            "url",
            "summary",
            "keywords",
            "named_entities",
        ]
    }
    expected_response["created_at"] = expected_response[
        "created_at"
    ].timestamp()
    expected_response["updated_at"] = expected_response[
        "updated_at"
    ].timestamp()

    response = topicaxis_api_client.get(
        "/v2/articles",
        params={"query": published_article.title},
        headers={"apikey": user.api_key},
    )

    assert response.status_code == 200
    assert response.json() == {"articles": [expected_response]}


def test_search_articles_with_categories(
    topicaxis_api_client, user, published_article
):
    expected_response = {
        key: getattr(published_article, key)
        for key in [
            "categories",
            "channels",
            "created_at",
            "updated_at",
            "description",
            "id",
            "image",
            "source",
            "tags",
            "title",
            "url",
            "summary",
            "keywords",
            "named_entities",
        ]
    }
    expected_response["created_at"] = expected_response[
        "created_at"
    ].timestamp()
    expected_response["updated_at"] = expected_response[
        "updated_at"
    ].timestamp()

    response = topicaxis_api_client.get(
        "/v2/articles",
        params={"categories": published_article.categories[0]["id"]},
        headers={"apikey": user.api_key},
    )

    assert response.status_code == 200
    assert response.json() == {"articles": [expected_response]}


def test_search_articles_with_source(
    topicaxis_api_client, user, published_article
):
    expected_response = {
        key: getattr(published_article, key)
        for key in [
            "categories",
            "channels",
            "created_at",
            "updated_at",
            "description",
            "id",
            "image",
            "source",
            "tags",
            "title",
            "url",
            "summary",
            "keywords",
            "named_entities",
        ]
    }
    expected_response["created_at"] = expected_response[
        "created_at"
    ].timestamp()
    expected_response["updated_at"] = expected_response[
        "updated_at"
    ].timestamp()

    response = topicaxis_api_client.get(
        "/v2/articles",
        params={"source": published_article.source["id"]},
        headers={"apikey": user.api_key},
    )

    assert response.status_code == 200
    assert response.json() == {"articles": [expected_response]}


def test_search_articles_with_tags(
    topicaxis_api_client, user, published_article
):
    expected_response = {
        key: getattr(published_article, key)
        for key in [
            "categories",
            "channels",
            "created_at",
            "updated_at",
            "description",
            "id",
            "image",
            "source",
            "tags",
            "title",
            "url",
            "summary",
            "keywords",
            "named_entities",
        ]
    }
    expected_response["created_at"] = expected_response[
        "created_at"
    ].timestamp()
    expected_response["updated_at"] = expected_response[
        "updated_at"
    ].timestamp()

    response = topicaxis_api_client.get(
        "/v2/articles",
        params={"tags": published_article.tags[0]["id"]},
        headers={"apikey": user.api_key},
    )

    assert response.status_code == 200
    assert response.json() == {"articles": [expected_response]}


def test_search_articles_with_channels(
    topicaxis_api_client, user, published_article
):
    expected_response = {
        key: getattr(published_article, key)
        for key in [
            "categories",
            "channels",
            "created_at",
            "updated_at",
            "description",
            "id",
            "image",
            "source",
            "tags",
            "title",
            "url",
            "summary",
            "keywords",
            "named_entities",
        ]
    }
    expected_response["created_at"] = expected_response[
        "created_at"
    ].timestamp()
    expected_response["updated_at"] = expected_response[
        "updated_at"
    ].timestamp()

    response = topicaxis_api_client.get(
        "/v2/articles",
        params={"channels": published_article.channels[0]["id"]},
        headers={"apikey": user.api_key},
    )

    assert response.status_code == 200
    assert response.json() == {"articles": [expected_response]}


def test_search_articles_with_from_date(
    topicaxis_api_client, user, published_article
):
    expected_response = {
        key: getattr(published_article, key)
        for key in [
            "categories",
            "channels",
            "created_at",
            "updated_at",
            "description",
            "id",
            "image",
            "source",
            "tags",
            "title",
            "url",
            "summary",
            "keywords",
            "named_entities",
        ]
    }
    expected_response["created_at"] = expected_response[
        "created_at"
    ].timestamp()
    expected_response["updated_at"] = expected_response[
        "updated_at"
    ].timestamp()

    response = topicaxis_api_client.get(
        "/v2/articles",
        params={
            "from_date": (
                published_article.created_at - timedelta(seconds=1)
            ).strftime("%Y-%m-%dT%H:%M:%S")
        },
        headers={"apikey": user.api_key},
    )

    assert response.status_code == 200
    assert response.json() == {"articles": [expected_response]}


def test_search_articles_with_to_date(
    topicaxis_api_client, user, published_article
):
    expected_response = {
        key: getattr(published_article, key)
        for key in [
            "categories",
            "channels",
            "created_at",
            "updated_at",
            "description",
            "id",
            "image",
            "source",
            "tags",
            "title",
            "url",
            "summary",
            "keywords",
            "named_entities",
        ]
    }
    expected_response["created_at"] = expected_response[
        "created_at"
    ].timestamp()
    expected_response["updated_at"] = expected_response[
        "updated_at"
    ].timestamp()

    response = topicaxis_api_client.get(
        "/v2/articles",
        params={
            "to_date": (
                published_article.created_at + timedelta(seconds=1)
            ).strftime("%Y-%m-%dT%H:%M:%S")
        },
        headers={"apikey": user.api_key},
    )

    assert response.status_code == 200
    assert response.json() == {"articles": [expected_response]}
