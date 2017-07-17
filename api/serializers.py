from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField
import rest_auth
from django.contrib.auth.models import Group, User

from .models import Jog, USER_ADMIN_GROUP_NAME, USER_MANAGER_GROUP_NAME


class JogSerializer(ModelSerializer):
    class Meta:
        model = Jog
        fields = ('id', 'date', 'distance_in_feet', 'time_in_seconds',
                  'created', 'modified')


class UserSerializer(ModelSerializer):
    role = SerializerMethodField(source='get_role')

    group_map = {
        'admin': USER_ADMIN_GROUP_NAME,
        'manager': USER_MANAGER_GROUP_NAME
    }

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        user = User.objects.create_user(**validated_data)
        group_name = self.group_map.get(role, None)
        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        return user

    def update(self, user, validated_data):
        # remove the rold from the validate data
        role = validated_data.pop('role', None)

        # set user attributes from remaining data
        for key, value in validated_data.items():
            setattr(user, key, value)

        # set the group from the role
        group_name = self.group_map.get(role, None)
        if group_name:
            # remove from all groups
            user.groups.clear()
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        elif role == 'user':
            # remove from all groups
            user.groups.clear()

        return user

    def get_role(self, user):
        groups = {g.name for g in user.groups.all()}
        if USER_ADMIN_GROUP_NAME in groups:
            return 'admin'
        elif USER_MANAGER_GROUP_NAME in groups:
            return 'manager'

        return 'user'

    class Meta:
        model = User
        fields = ('id', 'username', 'role')


class LoginSerializer(rest_auth.serializers.LoginSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        extra_kwargs = {
            "password": {
                "error_messages": {
                    "blank": "The password field is required",
                    "required": "The password field is required"
                }
            }
        }
        # read_only_fields = ('user', )


class TokenSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    token = CharField(source='key')

    class Meta:
        model = rest_auth.models.TokenModel
        fields = ('token', 'user')
