from operator import attrgetter


def test_get_sources_when_there_are_no_articles(topicaxis_api_client, user):
    response = topicaxis_api_client.get(
        "/v2/sources", headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {
        "sources": [],
    }


def test_get_sources(topicaxis_api_client, published_sources, user):
    response = topicaxis_api_client.get(
        "/v2/sources", headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {
        "sources": [
            {
                "id": source.id,
                "name": source.name,
                "url": source.url,
            }
            for source in sorted(published_sources, key=attrgetter("name"))
        ]
    }


def test_get_sources_with_limit(topicaxis_api_client, published_sources, user):
    response = topicaxis_api_client.get(
        "/v2/sources", params={"limit": 1}, headers={"apikey": user.api_key}
    )
    expected_source = sorted(published_sources, key=attrgetter("name"))[0]

    assert response.status_code == 200
    assert response.json() == {
        "sources": [
            {
                "id": expected_source.id,
                "name": expected_source.name,
                "url": expected_source.url,
            }
        ]
    }


def test_get_sources_with_offset(
    topicaxis_api_client, published_sources, user
):
    response = topicaxis_api_client.get(
        "/v2/sources", params={"offset": 1}, headers={"apikey": user.api_key}
    )
    expected_source = sorted(published_sources, key=attrgetter("name"))[1]

    assert response.status_code == 200
    assert response.json() == {
        "sources": [
            {
                "id": expected_source.id,
                "name": expected_source.name,
                "url": expected_source.url,
            }
        ]
    }


def test_get_sources_with_invalid_limit(topicaxis_api_client, user):
    response = topicaxis_api_client.get(
        "/v2/sources", params={"limit": -1}, headers={"apikey": user.api_key}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid request."}


def test_get_sources_with_invalid_offset(topicaxis_api_client, user):
    response = topicaxis_api_client.get(
        "/v2/sources", params={"offset": -1}, headers={"apikey": user.api_key}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid request."}


def test_get_sources_with_out_of_bounds_offset(
    topicaxis_api_client, published_sources, user
):
    response = topicaxis_api_client.get(
        "/v2/sources",
        params={"offset": 100000},
        headers={"apikey": user.api_key},
    )

    assert response.status_code == 200
    assert response.json() == {"sources": []}
