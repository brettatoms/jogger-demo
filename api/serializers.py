from rest_framework.serializers import CurrentUserDefault, ModelSerializer, \
    PrimaryKeyRelatedField
from .models import Jog


class JogSerializer(ModelSerializer):
    class Meta:
        model = Jog
        fields = ('id', 'date', 'distance_in_feet', 'time_in_seconds',
                  'created', 'modified')
