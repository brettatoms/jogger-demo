from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from ..models import Jog
from ..serializers import JogSerializer


class JogList(APIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (JSONParser, )

    def get(self, request):
        # get jogs for current user
        jogs = Jog.objects.filter(user=request.user)
        serializer = JogSerializer(jogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JogDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, jog_id):
        jog = get_object_or_404(Jog, id=jog_id, user=request.user)
        serializer = JogSerializer(jog)
        return Response(serializer.data)

    def put(self, request, jog_id):
        jog = get_object_or_404(Jog, id=jog_id, user=request.user)
        serializer = JogSerializer(jog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, jog_id):
        jog = get_object_or_404(Jog, id=jog_id, user=request.user)
        jog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
