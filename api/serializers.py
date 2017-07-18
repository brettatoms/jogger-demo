from rest_framework.serializers import CharField, ChoiceField, ModelSerializer
import rest_auth

from .models import Jog, User, USER_ROLES


class JogSerializer(ModelSerializer):
    class Meta:
        model = Jog
        fields = ('id', 'date', 'distance_in_feet', 'time_in_seconds',
                  'created', 'modified')


class UserSerializer(ModelSerializer):
    role = ChoiceField(USER_ROLES)

    def to_representation(self, user):
        # set class to our proxied user class
        user.__class__ = User
        super().to_representation(user)

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        user = User.objects.create_user(**validated_data)
        user.role = role
        return user

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
