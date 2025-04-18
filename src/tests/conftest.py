import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.database import engine, SessionLocal
from src.models.news import Base
from src.config import settings


@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def access_token(test_client):
    response = test_client.post(
        "/token",
        json={"client_id": settings.CLIENT_ID, "client_secret": settings.CLIENT_SECRET},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]
