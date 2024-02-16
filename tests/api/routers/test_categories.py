def test_get_categories_when_there_are_no_articles(topicaxis_api_client, user):
    response = topicaxis_api_client.get(
        "/v2/categories", headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {
        "categories": [],
    }


def test_get_categories(topicaxis_api_client, published_category, user):
    response = topicaxis_api_client.get(
        "/v2/categories", headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {
        "categories": [
            {
                "id": published_category.id,
                "name": published_category.name,
                "taxonomy": published_category.taxonomy,
            }
        ]
    }
