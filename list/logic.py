from django.db.models import Count, Q
from .models import Task, List
from django.shortcuts import get_object_or_404


# LIST LOGIC
def get_user_lists(user):
    lists = List.objects.filter(user=user)
    return lists


def get_list_details(list_id):
    queryset = List.objects.filter(
        id=list_id).annotate(completed_tasks=Count('tasks', Q(tasks__is_completed=True)), total_tasks=Count('tasks'))
    return get_object_or_404(queryset)


# TASKS LOGIC
def get_list_tasks(list_id):
    tasks = Task.objects.filter(list_id=list_id).select_related('list')
    return tasks


def get_task_details(task_id):
    task_details = get_object_or_404(Task.objects.select_related("list__user"), id=task_id)
    return task_details
