from datetime import date
from random import randint
import secrets

# from django.utils import timezone
import pytest
from django.contrib.auth.models import Group, Permission
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import Jog, User, USER_ADMIN_GROUP_NAME, USER_MANAGER_GROUP_NAME


@pytest.fixture()
def password():
    return secrets.token_urlsafe(8)


@pytest.fixture()
def user(django_user_model, password):
    # user = django_user_model.objects.create_user(
    user = User.objects.create_user(username='testy', password=password)
    Token.objects.create(user=user)
    return user


@pytest.fixture()
def user2(django_user_model, password):
    # user = django_user_model.objects.create_user(
    user = User.objects.create_user(username='testy2', password=password)
    Token.objects.create(user=user)
    return user


@pytest.fixture()
def user_manager_permissions():
    return [
        'list_users', 'view_user', 'add_user', 'change_user', 'delete_user'
    ]


@pytest.fixture()
def user_admin_permissions(user_manager_permissions):
    return user_manager_permissions + [
        'list_jogs', 'view_jog', 'add_jog', 'change_jog', 'delete_jog'
    ]


@pytest.fixture()
def admin_user(user, user_admin_permissions):
    group = Group.objects.get(name=USER_ADMIN_GROUP_NAME)
    user.groups.add(group)
    perms = Permission.objects.filter(codename__in=user_admin_permissions)
    group.permissions.add(*perms)
    return user


@pytest.fixture()
def manager_user(user, user_manager_permissions):
    group = Group.objects.get(name=USER_MANAGER_GROUP_NAME)
    user.groups.add(group)
    perms = Permission.objects.filter(codename__in=user_manager_permissions)
    group.permissions.add(*perms)
    return user


@pytest.fixture()
def user_password(user, password):
    user.set_password(password)
    return user, password


@pytest.fixture()
def client_user(client, user, password):
    assert client.login(username=user.username, password=password)
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
