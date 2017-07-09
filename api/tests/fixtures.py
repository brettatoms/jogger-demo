from datetime import date
import secrets

# from django.utils import timezone
import pytest
from random import randint
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import Jog


@pytest.fixture()
def password():
    return secrets.token_urlsafe(8)


@pytest.fixture()
def user(django_user_model, password):
    user = django_user_model.objects.create_user(
        username='testy', password=password)
    Token.objects.create(user=user)
    return user


@pytest.fixture()
def user_password(django_user_model, password):
    user = django_user_model.objects.create_user(
        username='testy', email='testy@test.com', password=password)
    return user, password


@pytest.fixture()
def client_user(client, user, password):
    assert client.login(username=user.username, password=password)
    print(client)
    return client


@pytest.fixture()
def api_client(user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
    return client


@pytest.fixture()
def jog(user):
    today = date.today()
    jog = Jog(
        user=user,
        date='{}-{}-{}'.format(today.year, today.month, today.day),
        distance_in_feet=randint(0, 1000),
        time_in_seconds=randint(0, 1000))
    jog.save()
    return jog
