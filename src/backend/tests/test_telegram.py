import pytest
from fastapi.testclient import TestClient
from server import fast_app_start

@pytest.fixture
def client():
    app = fast_app_start()
    return TestClient(app)

def test_info(client):
    params = {
        'innerWidth': 'test',
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
         'page_load_time': 'test'
    }
    response = client.post("/api/telegram/info", json=params)
    assert response.status_code == 200

def test_message(client):
    params = {
        "author": "test",
        "email": "test",
        "message": "test",
        "name": "test"
    }
    response = client.post("/api/telegram/message", json=params)
    assert response.status_code == 200
