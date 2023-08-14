from rest_framework_nested import routers
from django.urls import path, include
from . import views
from .views import TasksViewSet

router = routers.DefaultRouter()
router.register('tasks', views.TasksViewSet, basename='tasks')

urlpatterns = router.urls
