from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_mock_response():
    # Test creating a mock response
    response = client.post(
        "/mock-response", json={"path_template": "/user/{}/details", "response": {"status": "success"}}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Mock response set for path: /user/{}/details"}


def test_get_mock_response_with_valid_path():
    # Create mock responses
    response = client.post(
        "/mock-response", json={"path_template": "/user/{}/details", "response": {"status": "success"}}
    )
    assert response.status_code == 200  # Ensure the creation worked

    # Test retrieving the mocked response for specific dynamic values
    response = client.get("/user/123/details")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


def test_get_mock_response_with_non_matching_path():
    # Create a mock response
    client.post("/mock-response", json={"path_template": "/user/{}/details", "response": {"status": "success"}})

    # Test with a path that does not match the registered mock
    response = client.get("/user/123/not-details")
    assert response.status_code == 200
    assert response.json() == {"message": "Request received and logged."}


def test_create_another_mock_response():
    # Test creating a different mock response
    response = client.post(
        "/mock-response", json={"path_template": "/product/{}/info", "response": {"status": "product found"}}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Mock response set for path: /product/{}/info"}


def test_get_another_mock_response_with_valid_path():
    # Test retrieving the mocked response for another path
    response = client.get("/product/456/info")
    assert response.status_code == 200
    assert response.json() == {"status": "product found"}

    response = client.get("/product/ABC/info")
    assert response.status_code == 200
    assert response.json() == {"status": "product found"}


def test_get_another_mock_response_with_non_matching_path():
    # Test with a non-matching path for the new mock
    client.post("/mock-response", json={"path_template": "/product/{}/info", "response": {"status": "product found"}})
    response = client.get("/product/456/details")
    assert response.status_code == 200
    assert response.json() == {"message": "Request received and logged."}
