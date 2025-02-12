import pytest
from fastapi.testclient import TestClient
from server import create_fastapi_app

@pytest.fixture
def client():
    app = create_fastapi_app()
    return TestClient(app)

def test_418(client):
    response = client.get("/418")
    assert response.status_code == 200

def test_404(client):
    response = client.get("/404")
    assert response.status_code == 200
