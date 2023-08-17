from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class List(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')


class Task(models.Model):
    is_completed = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='task')












