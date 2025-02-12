import pytest
from fastapi.testclient import TestClient
from server import create_fastapi_app

@pytest.fixture
def client():
    app = create_fastapi_app()
    return TestClient(app)

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_home(client):
    response = client.get("/index")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_contact(client):
    response = client.get("/contact")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_project(client):
    response = client.get("/project")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_tou(client):
    response = client.get("/terms_of_use")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_privacy(client):
    response = client.get("/privacy_policy")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_cookie_policy(client):
    response = client.get("/cookie_policy")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_content_used(client):
    response = client.get("/content_used")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_robots(client):
    response = client.get("/robots.txt")
    assert response.status_code == 200

def test_sitemap(client):
    response = client.get("/sitemap.xml")
    assert response.status_code == 200