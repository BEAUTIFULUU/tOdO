from rest_framework_nested import routers
from django.urls import path, include
from . import views
from .views import ListView


urlpatterns = [
    path('lists/', ListView.as_view())
]








