from datetime import date
import json
from random import randint
import secrets

from .fixtures import *  # noqa
from ..models import Jog

# TODO: make sure we can't delete a jog that belongs to someone else
# TODO: test routes don't work if not logged in


def test_get_jog_list(jog, user2, api_client):
    Jog(date=date.today(), distance_in_feet=1, time_in_seconds=1,
        user=user2).save()
    response = api_client.get('/api/jogs/')
    assert response.status_code == 200
    data = json.loads(response.content)
    # should only get the jobs for the current user
    assert len(data) == 1
    assert data[0]['id'] == jog.id
    assert data[0]['distance_in_feet'] == jog.distance_in_feet
    assert data[0]['time_in_seconds'] == jog.time_in_seconds


def test_get_empty_jog_list(api_client):
    response = api_client.get('/api/jogs/')
    assert response.status_code == 200
    assert response.content == b'[]'


def test_get_jog_list_of_other_user_fail(api_client, jog, user2):
    response = api_client.get('/api/users/{}/jogs/'.format(user2.id))
    assert response.status_code == 403


def test_get_jog_list_of_other_user_as_admin(api_client, jog, admin_user,
                                             user2):
    response = api_client.get('/api/users/{}/jogs/'.format(user2.id))
    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data) == 1
    assert data[0]['id'] == jog.id
    assert data[0]['distance_in_feet'] == jog.distance_in_feet
    assert data[0]['time_in_seconds'] == jog.time_in_seconds
    assert data[0]['time_in_seconds'] == jog.time_in_seconds


def test_get_jog_detail(api_client, jog):
    response = api_client.get('/api/jogs/{}/'.format(jog.id))
    data = json.loads(response.content)
    assert response.status_code == 200, data
    assert data['id'] == jog.id


def test_get_jog_detail_of_other_user_as_admin(api_client, jog, admin_user,
                                               user2):
    jog_user2 = Jog(
        date=date.today(), distance_in_feet=1, time_in_seconds=1, user=user2)
    jog_user2.save()
    response = api_client.get('/api/jogs/{}/'.format(jog_user2.id))
    data = json.loads(response.content)
    assert response.status_code == 200, data
    assert data['id'] == jog_user2.id


def test_get_jog_detail_permissions_fail(django_user_model, api_client):
    password = secrets.token_urlsafe(8)
    user2 = django_user_model.objects.create_user(
        username='testy2', password=password)
    today = date.today()
    jog2 = Jog(
        user=user2,
        date='{}-{}-{}'.format(today.year, today.month, today.day),
        distance_in_feet=randint(0, 1000),
        time_in_seconds=randint(0, 1000))
    jog2.save()

    response = api_client.get('/api/jogs/{}/'.format(jog2.id))
    data = json.loads(response.content)
    assert response.status_code == 403, data


def test_post_jog(api_client):
    today = date.today()
    data = {
        'date': '{}-{}-{}'.format(today.year, today.month, today.day),
        'distance_in_feet': randint(1, 1000),
        'time_in_seconds': randint(1, 1000)
    }
    response = api_client.post('/api/jogs/', data=data, format='json')
    response_data = json.loads(response.content)
    assert response.status_code == 201, response_data
    assert isinstance(response_data['id'], int)
    # assert response_data['date'] == data['date']
    assert response_data['distance_in_feet'] == data['distance_in_feet']
    assert response_data['time_in_seconds'] == data['time_in_seconds']


def test_post_jog_as_admin(api_client, admin_user, user2):
    today = date.today()
    data = {
        'date': '{}-{}-{}'.format(today.year, today.month, today.day),
        'distance_in_feet': randint(1, 1000),
        'time_in_seconds': randint(1, 1000)
    }
    # create jog for other user
    response = api_client.post(
        '/api/users/{}/jogs/'.format(user2.id), data=data, format='json')
    response_data = json.loads(response.content)
    assert response.status_code == 201, response_data
    assert isinstance(response_data['id'], int)
    assert response_data['distance_in_feet'] == data['distance_in_feet']
    assert response_data['time_in_seconds'] == data['time_in_seconds']
    assert Jog.objects.get(id=response_data['id']).user.id == user2.id


def test_put_jog(api_client, jog):
    today = date.today()
    data = {
        'date': '{}-{}-{}'.format(today.year, today.month, today.day),
        'distance_in_feet': randint(1, 1000),
        'time_in_seconds': randint(1, 1000)
    }
    response = api_client.put(
        '/api/jogs/{}/'.format(jog.id), data=data, format='json')
    response_data = json.loads(response.content)
    assert response.status_code == 200, response_data
    assert isinstance(response_data['id'], int)
    # assert response_data['date'] == data['date']
    assert response_data['distance_in_feet'] == data['distance_in_feet']
    assert response_data['time_in_seconds'] == data['time_in_seconds']


def test_delete_jog(api_client, jog):
    response = api_client.delete('/api/jogs/{}/'.format(jog.id))
    assert response.status_code == 204


def test_fail_delete_missing_jog(api_client):
    response = api_client.delete('/api/jogs/{}/'.format(randint(1, 1000)))
    assert response.status_code == 404
