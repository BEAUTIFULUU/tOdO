from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions, request
from .models import Task
from .serializers import TaskSerializer


class TasksViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user__id=self.request.user.id)

