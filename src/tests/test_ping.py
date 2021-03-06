from starlette.testclient import TestClient


def test_ping(test_app):
    response = test_app.get('/ping')
    assert response.status_code == 200
    assert response.json() == {'ping': 'pong'}


def test_async_ping(test_app):
    response = test_app.get('/async-ping')
    assert response.status_code == 200
    assert response.json() == {'async-ping': 'async-pong'}
