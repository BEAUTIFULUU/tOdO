from django.db.models import Count
from rest_framework import serializers
from .models import Task, List


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'date']


class CreateUpdateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['date']


class ListDetailSerializer(serializers.ModelSerializer):
    completed_tasks = serializers.ReadOnlyField()
    total_tasks = serializers.ReadOnlyField()

    class Meta:
        model = List
        fields = ['id', 'date', 'total_tasks', 'completed_tasks']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'is_completed', 'title', 'description', 'tag']


class CreateUpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_completed', 'title', 'description', 'tag']
