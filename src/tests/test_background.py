from fastapi.testclient import TestClient
from src.config.config import settings

settings.DEBUG = True

class TestBackground:

    def __init__(self, app):
        self.client = TestClient(app)

    def run_tests(self):
        self.test_background()

    def test_background(self):
        response = self.client.get("/background")
        assert response.status_code == 200
