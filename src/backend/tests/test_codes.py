import pytest
from fastapi.testclient import TestClient
from server import fast_app_start

@pytest.fixture
def client():
    app = fast_app_start()
    return TestClient(app)

def test_418(client):
    response = client.get("/418")
    assert response.status_code == 200

def test_404(client):
    response = client.get("/404")
    assert response.status_code == 200
