from fastapi.testclient import TestClient
from main import app, mock_responses  # Import mock_responses to clear it

client = TestClient(app)

# Helper function to clear mocks before each test
def setup_function():
    mock_responses.clear()

def test_create_mock_response():
    setup_function()
    payload = {
        "path_template": "/user/{}/details",
        "method": "GET",
        "response": {
            "body": {"status": "success"},
            "status_code": 200
        }
    }
    response = client.post("/mock-response", json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "Mock response set for METHOD: GET, PATH: /user/{}/details"}

def test_get_mock_response_with_valid_path():
    setup_function()
    # Create mock response
    mock_config = {
        "path_template": "/user/{}/details",
        "method": "GET",
        "response": {
            "body": {"status": "success", "id": "123"},
            "status_code": 200
        }
    }
    create_response = client.post("/mock-response", json=mock_config)
    assert create_response.status_code == 201

    # Test retrieving the mocked response
    response = client.get("/user/123/details")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "id": "123"}

    # Test with another dynamic value
    mock_config_2 = {
        "path_template": "/user/{}/profile", # Different path
        "method": "GET",
        "response": {
            "body": {"profile_status": "active"},
            "status_code": 202 # Different status
        }
    }
    create_response_2 = client.post("/mock-response", json=mock_config_2)
    assert create_response_2.status_code == 201
    
    response_2 = client.get("/user/456/profile")
    assert response_2.status_code == 202
    assert response_2.json() == {"profile_status": "active"}


def test_get_mock_response_with_non_matching_path():
    setup_function()
    # Create a mock response
    mock_config = {
        "path_template": "/user/{}/details",
        "method": "GET",
        "response": {
            "body": {"status": "success"},
            "status_code": 200
        }
    }
    create_response = client.post("/mock-response", json=mock_config)
    assert create_response.status_code == 201

    # Test with a path that does not match the registered mock
    response = client.get("/user/123/not-details")
    assert response.status_code == 404
    expected_message = "Request for GET /user/123/not-details received and logged. No specific mock found."
    assert response.json() == {"message": expected_message}

def test_create_mock_for_post_request():
    setup_function()
    payload = {
        "path_template": "/product/{}/info",
        "method": "POST",
        "response": {
            "body": {"status": "product created", "id": "xyz"},
            "status_code": 201,
            "custom_headers": {"X-Product-ID": "xyz"}
        }
    }
    response = client.post("/mock-response", json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "Mock response set for METHOD: POST, PATH: /product/{}/info"}

    # Test retrieving the mocked POST response
    retrieved_response = client.post("/product/abc/info", json={"name": "Test Product"})
    assert retrieved_response.status_code == 201
    assert retrieved_response.json() == {"status": "product created", "id": "xyz"}
    assert retrieved_response.headers["x-product-id"] == "xyz"


def test_get_another_mock_response_with_valid_path_and_different_method():
    setup_function()
    # Mock for GET
    client.post(
        "/mock-response",
        json={
            "path_template": "/product/{}/info",
            "method": "GET",
            "response": {"body": {"status": "product found via GET"}, "status_code": 200},
        },
    )
    # Mock for PUT on the same path
    client.post(
        "/mock-response",
        json={
            "path_template": "/product/{}/info",
            "method": "PUT",
            "response": {"body": {"status": "product updated via PUT"}, "status_code": 202},
        },
    )

    # Test GET
    response_get = client.get("/product/456/info")
    assert response_get.status_code == 200
    assert response_get.json() == {"status": "product found via GET"}

    # Test PUT
    response_put = client.put("/product/456/info", json={"name": "Updated Name"})
    assert response_put.status_code == 202
    assert response_put.json() == {"status": "product updated via PUT"}
    
    # Test non-mocked method (e.g. DELETE) on same path
    response_delete = client.delete("/product/456/info")
    assert response_delete.status_code == 404


def test_get_another_mock_response_with_non_matching_path():
    setup_function()
    # Create a mock response
    mock_config = {
        "path_template": "/product/{}/info",
        "method": "GET",
        "response": {
            "body": {"status": "product found"},
            "status_code": 200
        }
    }
    create_response = client.post("/mock-response", json=mock_config)
    assert create_response.status_code == 201

    # Test with a non-matching path for the new mock
    response = client.get("/product/456/details") # 'details' instead of 'info'
    assert response.status_code == 404
    expected_message = "Request for GET /product/456/details received and logged. No specific mock found."
    assert response.json() == {"message": expected_message}

def test_mock_with_custom_headers():
    setup_function()
    payload = {
        "path_template": "/header-test",
        "method": "GET",
        "response": {
            "body": {"header_check": "present"},
            "status_code": 200,
            "custom_headers": {"X-Test-Header": "TestValue123", "X-Another": "Value"}
        }
    }
    create_response = client.post("/mock-response", json=payload)
    assert create_response.status_code == 201

    response = client.get("/header-test")
    assert response.status_code == 200
    assert response.json() == {"header_check": "present"}
    assert response.headers["x-test-header"] == "TestValue123"
    assert response.headers["x-another"] == "Value"
