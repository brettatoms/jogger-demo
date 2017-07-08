from django.db import models
from django.contrib.auth.models import User


class Jog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # the date the jog occured
    date = models.DateField()

    # the distance of the jog
    distance_in_feet = models.IntegerField()

    # how long the jog took in seconds
    time_in_seconds = models.IntegerField()
