from rest_framework import filters
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from .serializers import TaskSerializer, ListSerializer, CreateUpdateListSerializer, ListDetailSerializer, \
    CreateUpdateTaskSerializer
from .logic import get_user_lists, get_list_details, get_list_tasks, get_task_details


class ListView(generics.ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']

    def get_queryset(self):
        return get_user_lists(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CreateUpdateListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class ListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'list_id'

    def get_object(self):
        list_id = self.kwargs['list_id']
        return get_list_details(list_id)

    def update(self, request, *args, **kwargs):
        update_list = self.get_object()
        serializer = self.get_serializer(update_list, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)


class TaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_completed', 'tag']

    def get_queryset(self):
        tasks = get_list_tasks(list_id=self.kwargs['list_id'])
        return tasks

    def create(self, request, *args, **kwargs):
        serializer = CreateUpdateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(list_id=self.kwargs['list_id'])
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateUpdateTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'task_id'

    def get_object(self):
        task_id = self.kwargs['task_id']
        return get_task_details(task_id=task_id)
