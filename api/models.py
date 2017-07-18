from django.db import models
from rest_framework.serializers import ValidationError
import django.contrib.auth as auth
from django_extensions.db.models import TimeStampedModel

USER_ADMIN_GROUP_NAME = 'User admin'
USER_MANAGER_GROUP_NAME = 'User manager'

USER_ROLES = {'admin', 'manager', 'user'}


class User(auth.models.User):
    group_map = {
        'admin': USER_ADMIN_GROUP_NAME,
        'manager': USER_MANAGER_GROUP_NAME
    }

    @property
    def role(self):
        groups = {g.name for g in self.groups.all()}
        if USER_ADMIN_GROUP_NAME in groups:
            return 'admin'
        elif USER_MANAGER_GROUP_NAME in groups:
            return 'manager'

        return 'user'

    @role.setter
    def role(self, role):
        if role not in USER_ROLES:
            raise ValidationError(
                'Role should be one of {}'.format(', '.joing(USER_ROLES)))

        group_name = self.group_map.get(role, None)
        if group_name:
            # remove from all groups
            self.groups.clear()
            group = auth.models.Group.objects.get(name=group_name)
            self.groups.add(group)
        elif role == 'user':
            # remove from all groups
            self.groups.clear()

    @role.deleter
    def role(self):
        self.groups.clear()

    class Meta:
        proxy = True
        permissions = (('list_users', 'Can list users'),
                       ('view_user', 'Can view user'))  # yapf: disable


class Jog(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # the date the jog occured
    date = models.DateField()

    # the distance of the jog
    distance_in_feet = models.IntegerField()

    # how long the jog took in seconds
    time_in_seconds = models.IntegerField()

    class Meta:
        ordering = ('created', )
        permissions = (('list_jogs', 'Can list jogs'),
                       ('view_jog', 'Can view jog'))  # yapf: disable
