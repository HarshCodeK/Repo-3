from fastapi.testclient import TestClient
from kaykay.app import app
def test_health(): assert TestClient(app).get("/health").json()["ok"] is True


def test_chat_requires_an_issued_key():
    response = TestClient(app).post("/v1/chat/completions", json={"prompt": "hello"})
    assert response.status_code == 401


def test_issued_key_allows_chat():
    client = TestClient(app)
    key = client.post("/v1/keys").json()["api_key"]
    response = client.post("/v1/chat/completions", headers={"X-API-Key": key}, json={"prompt": "hello"})
    assert response.status_code == 200
