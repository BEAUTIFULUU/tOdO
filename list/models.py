from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)


class Task(models.Model):

    is_completed = models.BooleanField(default=False)
    date = models.DateField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(Category, related_name='tasks', on_delete=models.CASCADE)


class Summary(models.Model):
    done = models.IntegerField(max_length=2)
    undone = models.IntegerField(max_length=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

