from rest_framework_nested import routers
from django.urls import path, include
from . import views
from .views import ListView, ListDetailView, TaskView, TaskDetailView

urlpatterns = [
    path('lists/', ListView.as_view(), name='create_list'),
    path('lists/<int:list_id>/', ListDetailView.as_view()),
    path('lists/<int:list_id>/tasks/', TaskView.as_view(), name='create_task'),
    path('lists/<int:list_id>/tasks/<int:task_id>/', TaskDetailView.as_view())
]








