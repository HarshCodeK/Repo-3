from fastapi.testclient import TestClient
from kaykay.app import app
def test_health(): assert TestClient(app).get("/health").json()["ok"] is True
