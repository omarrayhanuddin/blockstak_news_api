from src.config import settings


def test_token_endpoint(test_client):
    response = test_client.post(
        "/token",
        json={"client_id": settings.CLIENT_ID, "client_secret": settings.CLIENT_SECRET},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"


def test_invalid_credentials(test_client):
    response = test_client.post(
        "/token",
        json={"client_id": "wrong-id", "client_secret": "wrong-secret"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect client credentials"
