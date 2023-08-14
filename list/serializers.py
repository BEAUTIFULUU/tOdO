from rest_framework import serializers
from .models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer

    class Meta:
        model = Task
        fields = ['id', 'is_completed', 'date', 'title', 'category', 'description']
