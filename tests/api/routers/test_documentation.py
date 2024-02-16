def test_swagger_page_is_disabled(topicaxis_api_client):
    response = topicaxis_api_client.get("/docs")

    assert response.status_code == 404


def test_redoc_page_is_disabled(topicaxis_api_client):
    response = topicaxis_api_client.get("/redoc")

    assert response.status_code == 404


def test_openapi_json_page_is_disabled(topicaxis_api_client):
    response = topicaxis_api_client.get("/openapi.json")

    assert response.status_code == 404
