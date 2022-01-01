import json
import pytest
from app.api import crud


def test_create_todo(test_app, monkeypatch):
    test_request_payload = {'title': 'title1', 'description': 'desc1'}
    test_response_payload = {
        'id': 1, 'title': 'title1', 'description': 'desc1'}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, 'post', mock_post)
    response = test_app.post('/todos/', data=json.dumps(test_request_payload))
    assert response.status_code == 201
    assert response.json() == test_response_payload

    response = test_app.post(
        '/todos/', json={'title': 't', 'description': 'd'})
    assert response.status_code == 422


def test_create_invalid_todo(test_app):
    response = test_app.post('/todos/', data=json.dumps({'title': 'title2'}))
    assert response.status_code == 422


def test_read_todo(test_app, monkeypatch):
    test_data = {'id': 1, 'title': 'title1', 'description': 'desc1'}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, 'get', mock_get)

    response = test_app.get('/todos/1')
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_invalid_todo(test_app, monkeypatch):
    async def mock_get(id):
        return None
    monkeypatch.setattr(crud, 'get', mock_get)

    response = test_app.get('/todos/44')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Todo not found'

    response = test_app.get('/todos/0')
    assert response.status_code == 422


def test_read_todos(test_app, monkeypatch):
    test_data = [
        {'title': 'title1', 'description': 'desc1', 'id': 1},
        {'title': 'title2', 'description': 'desc2', 'id': 2},
        {'title': 'title3', 'description': 'desc3', 'id': 3},
    ]

    async def mock_get_all():
        return test_data

    # NOTE get_all defined in todos.py
    monkeypatch.setattr(crud, 'get_all', mock_get_all)

    response = test_app.get('/todos/')
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_todo(test_app, monkeypatch):
    test_update_data = {"title": "asd",
                        "description": "var", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/todos/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    'id, payload, status_code',
    [
        [1, {}, 422],
        [1, {'description': 'var'}, 422],
        [44, {'title': 'asd', 'description': 'var'}, 404],
        [1, {'title': 't', 'description': 'var'}, 422],
        [1, {'title': 'title1', 'description': 'd'}, 422],
        [0, {'title': 'title1', 'description': 'desc'}, 422],
    ],
)
def test_update_invalid_todo(test_app, monkeypatch, id, payload, status_code):
    async def monkey_get(id):
        return None

    monkeypatch.setattr(crud, 'get', monkey_get)
    response = test_app.put(f'/todos/{id}/', data=json.dumps(payload))
    assert response.status_code == status_code


def test_remove_todo(test_app, monkeypatch):
    test_data = {'title': 'foo', 'description': 'bar', 'id': 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, 'get', mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, 'delete', mock_delete)

    response = test_app.delete('/todos/1/')
    assert response.status_code == 200
    assert response.json() == test_data

    response = test_app.delete('/todos/0/')
    assert response.status_code == 422


def test_remove_invalid_todo(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, 'get', mock_get)

    response = test_app.delete('/todos/44/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Todo not found'
