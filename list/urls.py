from django.urls import path
from uuid import UUID
from .views import ListView, ListDetailView, TaskView, TaskDetailView

urlpatterns = [
    path('lists/', ListView.as_view(), name='get_create_list'),
    path('lists/<uuid:list_id>/', ListDetailView.as_view(), name='update_delete_list'),
    path('lists/<uuid:list_id>/tasks/', TaskView.as_view(), name='get_create_task'),
    path('lists/<uuid:list_id>/tasks/<uuid:task_id>/', TaskDetailView.as_view(), name='update_delete_task')
]








