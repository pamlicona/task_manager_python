from django.contrib.auth.models import User
from django.db import models


class TaskState(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)


class Duration(models.Model):
    name = models.CharField(max_length=50)
    create_date = models.DateField(auto_now_add=True)
    initial_range = models.IntegerField()
    final_range = models.IntegerField()
    active = models.BooleanField(default=True)


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(TaskState, default=5, on_delete=models.CASCADE)
    order = models.IntegerField()
    create_date = models.DateField(auto_now_add=True)
    final_date = models.DateField(auto_now_add=True, null=True, blank=True)
    initial_duration = models.CharField(max_length=30)
    time_left = models.CharField(max_length=30, null=True, blank=True)
    final_duration = models.CharField(max_length=30, null=True, blank=True)
    duration = models.ForeignKey(Duration, on_delete=models.CASCADE)
