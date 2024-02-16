def test_get_channels_when_there_are_no_articles(topicaxis_api_client, user):
    response = topicaxis_api_client.get(
        "/v2/channels", headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {
        "channels": [],
    }


def test_get_channels(topicaxis_api_client, published_channels, user):
    response = topicaxis_api_client.get(
        "/v2/channels", headers={"apikey": user.api_key}
    )

    assert response.status_code == 200
    assert response.json() == {
        "channels": [
            {
                "id": channel.id,
                "name": channel.name,
                "url": channel.url,
            }
            for channel in sorted(
                published_channels, key=lambda item: item.name
            )
        ]
    }
