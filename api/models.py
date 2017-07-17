from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel

USER_ADMIN_GROUP_NAME = 'User admin'
USER_MANAGER_GROUP_NAME = 'User manager'


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
