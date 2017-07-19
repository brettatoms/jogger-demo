import json
from random import randint

from .fixtures import *  # noqa


def test_get_user_list_as_admin(admin_user, api_client):
    response = api_client.get('/api/users/')
    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data) == 1
    assert data[0]['id'] == admin_user.id
    assert data[0]['username'] == admin_user.username
    assert data[0]['role'] == 'admin'


def test_get_user_list_as_manager(manager_user, api_client):
    response = api_client.get('/api/users/')
    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data) == 1
    assert data[0]['id'] == manager_user.id
    assert data[0]['username'] == manager_user.username
    assert data[0]['role'] == 'manager'


def test_get_user_list_permission_fail(user, api_client):
    response = api_client.get('/api/users/')
    assert response.status_code == 403


def test_get_user_detail(api_client, user):
    response = api_client.get('/api/users/{}/'.format(user.id))
    data = json.loads(response.content)
    assert response.status_code == 200, data
    assert data['id'] == user.id


def test_get_other_user_permissions_fail(api_client, user2):
    response = api_client.get('/api/users/{}/'.format(user2.id))
    assert response.status_code == 403


def test_get_other_user_as_manager(api_client, manager_user, user2):
    response = api_client.get('/api/users/{}/'.format(user2.id))
    data = json.loads(response.content)
    assert response.status_code == 200, data
    assert data['id'] == user2.id


def test_get_other_user_as_admin(api_client, admin_user, user2):
    response = api_client.get('/api/users/{}/'.format(user2.id))
    data = json.loads(response.content)
    assert response.status_code == 200, data
    assert data['id'] == user2.id


def test_post_user_as_admin(api_client, admin_user, password):
    request_data = {
        'username': 'test@toptal-jogger.com',
        'role': 'manager',
        'password': password
    }
    response = api_client.post('/api/users/', data=request_data, format='json')
    data = json.loads(response.content)
    assert response.status_code == 201, data
    assert isinstance(data['id'], int)
    assert data['username'] == request_data['username']
    assert data['role'] == request_data['role']


def test_post_user_as_manager(api_client, manager_user, password):
    request_data = {
        'username': 'test@toptal-jogger.com',
        'role': 'manager',
        'password': password
    }
    response = api_client.post('/api/users/', data=request_data, format='json')
    data = json.loads(response.content)
    assert response.status_code == 201, data
    assert isinstance(data['id'], int)
    assert data['username'] == request_data['username']
    assert data['role'] == request_data['role']


def test_put_user(api_client, user):
    request_data = {'username': 'newname', 'role': 'admin'}
    response = api_client.put(
        '/api/users/{}/'.format(user.id), data=request_data, format='json')
    data = json.loads(response.content)
    assert response.status_code == 200, data
    assert isinstance(data['id'], int)
    assert data['username'] == request_data['username']
    assert data['role'] == request_data['role']


def test_put_user_invalid_role(api_client, user):
    request_data = {'username': 'newname', 'role': 'badrole'}
    response = api_client.put(
        '/api/users/{}/'.format(user.id), data=request_data, format='json')
    data = json.loads(response.content)
    assert response.status_code == 400, data


def test_put_other_user_permissions_fail(api_client, user, user2):
    request_data = {'username': 'newname', 'role': 'admin'}
    response = api_client.put(
        '/api/users/{}/'.format(user2.id), data=request_data, format='json')
    assert response.status_code == 403


def test_put_other_user_as_manager(api_client, manager_user, user2):
    request_data = {'username': 'newname', 'role': 'admin'}
    response = api_client.put(
        '/api/users/{}/'.format(user2.id), data=request_data, format='json')
    assert response.status_code == 200


def test_put_other_user_as_admin(api_client, admin_user, user2):
    request_data = {'username': 'newname', 'role': 'admin'}
    response = api_client.put(
        '/api/users/{}/'.format(user2.id), data=request_data, format='json')
    assert response.status_code == 200


def test_delete_user(api_client, user):
    response = api_client.delete('/api/users/{}/'.format(user.id))
    assert response.status_code == 204


def test_delete_other_user_permissions_fail(api_client, user, user2):
    response = api_client.delete('/api/users/{}/'.format(user2.id))
    assert response.status_code == 403


def test_delete_other_user_as_manager(api_client, manager_user, user2):
    response = api_client.delete('/api/users/{}/'.format(user2.id))
    assert response.status_code == 204


def test_delete_other_user_as_admin(api_client, admin_user, user2):
    response = api_client.delete('/api/users/{}/'.format(user2.id))
    assert response.status_code == 204


def test_fail_delete_missing_user(api_client):
    response = api_client.delete('/api/users/{}/'.format(randint(1, 1000)))
    assert response.status_code == 404
