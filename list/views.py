from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions, request
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import Task, List
from .serializers import TasksSerializer, ListSerializer, CreateListSerializer
from .logic import get_user_lists


class ListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lists = get_user_lists(user=request.user)
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

    def put(self, request):
        serializer = CreateListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user.id)
        return Response(data=serializer.validated_data)
