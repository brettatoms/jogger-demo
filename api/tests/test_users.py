import json
from random import randint

from .fixtures import *  # noqa


def test_get_user_list(user, api_client):
    response = api_client.get('/api/users/')
    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data) == 1
    print(data)
    assert data[0]['id'] == user.id
    assert data[0]['username'] == user.username
    assert data[0]['role'] == 'user'


def test_get_user_detail(api_client, user):
    response = api_client.get('/api/users/{}/'.format(user.id))
    data = json.loads(response.content)
    assert response.status_code == 200, data
    assert data['id'] == user.id


def test_post_user(api_client):
    request_data = {'username': 'test@toptal-jogger.com', 'role': 'manager'}
    response = api_client.post('/api/users/', data=request_data, format='json')
    data = json.loads(response.content)
    assert response.status_code == 201, data
    assert isinstance(data['id'], int)
    assert data['username'] == request_data['username']
    assert data['role'] == request_data['role']


# def test_get_jog_detail_permissions_fail(django_user_model, api_client):
#     password = secrets.token_urlsafe(8)
#     user2 = django_user_model.objects.create_user(
#         username='testy2', password=password)
#     today = date.today()
#     jog2 = Jog(
#         user=user2,
#         date='{}-{}-{}'.format(today.year, today.month, today.day),
#         distance_in_feet=randint(0, 1000),
#         time_in_seconds=randint(0, 1000))
#     jog2.save()

#     response = api_client.get('/api/jogs/{}/'.format(jog2.id))
#     data = json.loads(response.content)
#     assert response.status_code == 404, data


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


def test_delete_user(api_client, user):
    response = api_client.delete('/api/users/{}/'.format(user.id))
    assert response.status_code == 204


def test_fail_delete_missing_user(api_client):
    response = api_client.delete('/api/users/{}/'.format(randint(1, 1000)))
    assert response.status_code == 404
