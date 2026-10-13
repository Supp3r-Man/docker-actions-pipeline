import pytest

from app.main import app


@pytest.fixture()
def client():
    return app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index_reports_version(client):
    body = client.get("/").get_json()
    assert body["message"].startswith("Hello")
    assert "version" in body


def test_greet(client):
    assert client.get("/greet/Ada").get_json() == {"greeting": "Hello, Ada!"}
