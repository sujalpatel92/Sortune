from fastapi.testclient import TestClient
from sortune_api.main import app


def test_health_endpoint_smoke():
    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
