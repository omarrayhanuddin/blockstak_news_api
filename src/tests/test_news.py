def test_get_news(test_client, access_token):
    response = test_client.get(
        "/news/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_save_latest_news(test_client, access_token):
    response = test_client.post(
        "/news/save-latest", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_headlines_by_country(test_client, access_token):
    response = test_client.get(
        "/news/headlines/country/us",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_headlines_by_source(test_client, access_token):
    response = test_client.get(
        "/news/headlines/source/bbc-news",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_headlines_filtered(test_client, access_token):
    response = test_client.get(
        "/news/headlines/filter?country=us&source=bbc-news",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_unauthorized_access(test_client):
    response = test_client.get("/news/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_invalid_token_format(test_client):
    response = test_client.get(
        "/news/", headers={"Authorization": "Bearer invalid.token.string"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"
