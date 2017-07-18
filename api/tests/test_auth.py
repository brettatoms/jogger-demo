import json

import pytest

from .fixtures import *  # noqa


@pytest.mark.django_db()
def test_registration(client, password):
    response = client.post(
        '/api/auth/register',
        json.dumps({
            'username': 'testy',
            'password1': password,
            'password2': password
        }),
        content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.content)
    assert isinstance(data.get('token'), str)


@pytest.mark.django_db()
def test_login(client, user_password):
    user, password = user_password
    response = client.post(
        '/api/auth/login/',
        json.dumps({
            'username': user.username,
            'password': password
        }),
        content_type='application/json')
    data = json.loads(response.content)
    assert response.status_code == 200
    assert isinstance(data.get('token'), str)


@pytest.mark.django_db()
def test_login_failed(client, user_password):
    user, password = user_password
    response = client.post(
        '/api/auth/login/',
        json.dumps({
            'username': user.username,
            'password': 'badpassword'
        }),
        content_type='application/json')
    assert response.status_code == 400


@pytest.mark.django_db()
def test_logout(client_user):
    response = client_user.post('/api/auth/logout/')
    assert response.status_code == 200
