from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class List(models.Model):
    date = models.DateField(null=False, blank=True, default=timezone.now().date())
    important_event = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')


class Task(models.Model):
    TAG_HOME = 'Home'
    TAG_SHOP = 'Shop'
    TAG_WORK = 'Work'
    TAG_FITNESS = 'Fitness'
    TAG_LEARNING = 'Learning'
    TAG_OTHER = 'Other'

    TAG_CHOICES = [
        (TAG_HOME, 'Home'),
        (TAG_SHOP, 'Shop'),
        (TAG_WORK, 'Work'),
        (TAG_FITNESS, 'Fitness'),
        (TAG_LEARNING, 'Learning'),
        (TAG_OTHER, 'Other')
    ]

    is_completed = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')
    tag = models.CharField(max_length=8, choices=TAG_CHOICES, default=TAG_OTHER, null=False)
