from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission

from ..models import Jog
from ..serializers import JogSerializer


class JogListPermission(BasePermission):
    def has_permission(self, request, view):
        check_method = getattr(
            self, 'check_{}_permissions'.format(request.method.lower()),
            lambda r, v: False)

        return check_method(request, view)

    def check_get_permissions(self, request, view):
        user_id = request.resolver_match.kwargs.get('user_id', None)
        if not user_id:
            return True

        return user_id == request.user.id or request.user.has_perm(
            'api.list_jogs')

    def check_post_permissions(self, request, view):
        user_id = request.resolver_match.kwargs.get('user_id', None)
        if not user_id:
            return True

        return user_id == request.user.id or request.user.has_perm(
            'api.add_jog')


class JogList(APIView):
    permission_classes = (IsAuthenticated, JogListPermission)

    def get(self, request, user_id=None):
        # get jogs for current user
        jogs = Jog.objects.filter(user=request.user)
        serializer = JogSerializer(jogs, many=True)
        return Response(serializer.data)

    def post(self, request, user_id=None):
        serializer = JogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JogDetailPermission(BasePermission):
    def has_object_permission(self, request, view, jog):
        check_method = getattr(
            self, 'check_{}_permissions'.format(request.method.lower()),
            lambda r, v: False)

        return check_method(request, view, jog)

    def check_get_permissions(self, request, view, jog):
        return jog.user == request.user or request.user.has_perm(
            'api.view_jog')

    def check_put_permissions(self, request, view, jog):
        return jog.user == request.user or request.user.has_perm(
            'api.change_jog')

    def check_delete_permissions(self, request, view, jog):
        return jog.user == request.user or request.user.has_perm(
            'api.delete_jog')


class JogDetail(APIView):
    permission_classes = (IsAuthenticated, JogDetailPermission)

    def get(self, request, jog_id):
        jog = get_object_or_404(Jog, id=jog_id)
        self.check_object_permissions(request, jog)
        serializer = JogSerializer(jog)
        return Response(serializer.data)

    def put(self, request, jog_id):
        jog = get_object_or_404(Jog, id=jog_id)
        self.check_object_permissions(request, jog)
        serializer = JogSerializer(jog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, jog_id):
        jog = get_object_or_404(Jog, id=jog_id)
        self.check_object_permissions(request, jog)
        jog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
