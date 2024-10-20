from fastapi.testclient import TestClient
from src.config.config import settings

settings.DEBUG = True

class TestPages:

    def __init__(self, app):
        self.client = TestClient(app)

    def run_tests(self):
        self.test_index()
        self.test_home()
        self.test_about()
        self.test_contact()
        self.test_project()
        self.test_tou()
        self.test_privacy()
        self.test_cookie_policy()
        self.test_content_used()
        self.test_robots()
        self.test_sitemap()

    def test_index(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text

    def test_home(self):
        response = self.client.get("/index")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text

    def test_about(self):
        response = self.client.get("/about")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text

    def test_contact(self):
        response = self.client.get("/contact")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text

    def test_project(self):
        response = self.client.get("/project")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text

    def test_tou(self):
        response = self.client.get("/terms_of_use")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text

    def test_privacy(self):
        response = self.client.get("/privacy_policy")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text

    def test_cookie_policy(self):
        response = self.client.get("/cookie_policy")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text

    def test_content_used(self):
        response = self.client.get("/content_used")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text

    def test_robots(self):
        response = self.client.get("/robots.txt")
        assert response.status_code == 200

    def test_sitemap(self):
        response = self.client.get("/sitemap.xml")
        assert response.status_code == 200