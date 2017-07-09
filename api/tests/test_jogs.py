from datetime import date
import json
from random import randint

from .fixtures import *  # noqa


def test_get_jog_list(jog, api_client):
    response = api_client.get('/api/jogs/')
    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data) == 1
    assert data[0]['id'] == jog.id
    assert data[0]['distance_in_feet'] == jog.distance_in_feet
    assert data[0]['time_in_seconds'] == jog.time_in_seconds


# TODO: make sure we only return jogs lists of the current user


def test_get_empty_jog_list(api_client):
    response = api_client.get('/api/jogs/')
    assert response.status_code == 200
    assert response.content == b'[]'


def test_get_jog_detail(api_client, jog):
    response = api_client.get('/api/jogs/{}/'.format(jog.id))
    data = json.loads(response.content)
    assert response.status_code == 200, data
    assert data['id'] == jog.id


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


# TODO: make sure we can't delete a jog that belongs to someone else
