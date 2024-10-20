from fastapi.testclient import TestClient
from src.config.config import settings

settings.DEBUG = True

class TestTelegram:

    def __init__(self, app):
        self.client = TestClient(app)

    def run_tests(self):
        self.test_info()
        self.test_message()

    def test_info(self):
        params = {
            {'innerWidth': 'test',
             'innerHeight': 'test',
             'screen_width': 'test',
             'screen_height': 'test',
             'userAgent': 'test',
             'platform': 'test',
             'language': 'test',
             'location_href': 'test',
             'connection_downlink': 'test',
             'connection_effective_type': 'test',
             'online': 'test',
             'performance_timing': 'test',
             'max_touch_points': 'test',
             'hardware_concurrency': 'test',
             'device_memory': 'test',
             'color_depth': 'test',
             'pixel_depth': 'test',
             'timezone': 'test',
             'cookies_enabled': 'test',
             'referrer': 'test',
             'visibility_state': 'test',
             'document_title': 'test',
             'page_load_time': 'test'}
        }
        response = self.client.post("/info", json=params)
        assert response.status_code == 200

    def test_message(self):
        params = {
            "author": "test",
            "email": "test",
            "message": "test",
            "name": "test"
        }
        response = self.client.post("/message", json=params)
        assert response.status_code == 200
