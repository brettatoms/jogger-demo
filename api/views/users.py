# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserPostSerializer, UserSerializer
from ..models import User


class UserListPermission(BasePermission):
    def has_permission(self, request, view):
        check_method = getattr(
            self, 'check_{}_permissions'.format(request.method.lower()),
            lambda r, v: False)

        return check_method(request, view)

    def check_get_permissions(self, request, view):
        return request.user.has_perm('auth.list_users')

    def check_post_permissions(self, request, view):
        return request.user.has_perm('auth.add_user')


class UserList(APIView):
    permission_classes = (IsAuthenticated, UserListPermission)

    def get(self, request):
        # get users for current user
        # users = User.objects.filter(user=request.user)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(role=request.data.pop('role', None))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailPermission(BasePermission):
    def has_object_permission(self, request, view, user):
        check_method = getattr(
            self, 'check_{}_permissions'.format(request.method.lower()),
            lambda r, v: False)

        return check_method(request, view, user)

    def check_get_permissions(self, request, view, user):
        return user == request.user or request.user.has_perm('auth.view_user')

    def check_put_permissions(self, request, view, user):
        return user == request.user or request.user.has_perm(
            'auth.change_user')

    def check_delete_permissions(self, request, view, user):
        return user == request.user or request.user.has_perm(
            'auth.delete_user')


class UserDetail(APIView):
    permission_classes = (IsAuthenticated, UserDetailPermission)

    def get(self, request, user_id):
        user = request.user if user_id == request.user.id else \
               get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = request.user if user_id == request.user.id else \
               get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = request.user if user_id == request.user.id else \
               get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        # user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
