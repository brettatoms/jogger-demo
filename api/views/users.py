from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_auth.serializers import UserDetailsSerializer

from django.contrib.auth.models import User

from ..models import USER_ADMIN_GROUP_NAME, USER_MANAGER_GROUP_NAME
from ..serializers import UserSerializer


class UserList(APIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (JSONParser, )

    def get(self, request):
        # get users for current user
        # users = User.objects.filter(user=request.user)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(role=request.data.pop('role', None))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save(role=request.data.pop('role', None))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
