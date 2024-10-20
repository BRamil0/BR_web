from fastapi.testclient import TestClient
from src.config.config import settings

settings.DEBUG = True

class TestCodes:

    def __init__(self, app):
        self.client = TestClient(app)

    def run_tests(self):
        self.test_418()
        self.test_404()

    def test_418(self):
        response = self.client.get("/418")
        assert response.status_code == 200

    def test_404(self):
        response = self.client.get("/404")
        assert response.status_code == 200
