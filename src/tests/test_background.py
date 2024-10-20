import pytest
from fastapi.testclient import TestClient
from main import fast_app_start

@pytest.fixture
def client():
    app = fast_app_start()
    return TestClient(app)

def test_background(client):
    response = client.get("/background")
    assert response.status_code == 200
