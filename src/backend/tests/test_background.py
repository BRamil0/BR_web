import pytest
from fastapi.testclient import TestClient
from server import create_fastapi_app

@pytest.fixture
def client():
    app = create_fastapi_app()
    return TestClient(app)

def test_background(client):
    response = client.get("/api/background")
    print(response.json())
    assert response.status_code == 200
