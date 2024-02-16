from operator import attrgetter


def test_get_tags_when_there_are_no_articles(topicaxis_api_client, user):
    response = topicaxis_api_client.get(
        "/v2/tags", headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {
        "tags": [],
    }


def test_get_tags(topicaxis_api_client, published_tags, user):
    response = topicaxis_api_client.get(
        "/v2/tags", headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {
        "tags": [
            {"id": tag.id, "name": tag.name}
            for tag in sorted(published_tags, key=attrgetter("name"))
        ]
    }
