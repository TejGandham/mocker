# tests/app/test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_log_requests_middleware():
    response = client.get("/test-endpoint")
    assert response.status_code == 200
    assert response.json() == {"message": "Request received and logged."}


def test_post_request_logging():
    response = client.post("/test-endpoint", json={"key": "value"})
    assert response.status_code == 200
    assert response.json() == {"message": "Request received and logged."}


def test_put_request_logging():
    response = client.put("/test-endpoint", json={"key": "updated value"})
    assert response.status_code == 200
    assert response.json() == {"message": "Request received and logged."}


def test_delete_request_logging():
    response = client.delete("/test-endpoint")
    assert response.status_code == 200
    assert response.json() == {"message": "Request received and logged."}


def test_patch_request_logging():
    response = client.patch("/test-endpoint", json={"key": "patched value"})
    assert response.status_code == 200
    assert response.json() == {"message": "Request received and logged."}
