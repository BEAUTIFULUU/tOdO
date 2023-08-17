from rest_framework import serializers
from .models import Task, List


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'date']


class CreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['date']


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_completed', 'title', 'description']
