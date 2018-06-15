from rest_framework import serializers
from .models import Task, TaskState, Duration
from user.serializer import UserSerializer


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskState
        fields = ('id', 'name', 'active', 'create_date')


class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = ('id', 'name', 'active', 'create_date')


class TaskSerializer(serializers.ModelSerializer):
    status = TaskStatusSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    duration = DurationSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'description',
            'user',
            'status',
            'order',
            'create_date',
            'final_date',
            'initial_duration',
            'time_left',
            'final_duration',
            'duration'
        )


class TaskUpdateSerializer(serializers.ModelSerializer):
    status = TaskStatusSerializer(read_only=True, required=False)
    user = UserSerializer(read_only=True, required=False)
    duration = DurationSerializer(read_only=True, required=False)

    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'description',
            'user',
            'status',
            'order',
            'create_date',
            'final_date',
            'initial_duration',
            'time_left',
            'final_duration',
            'duration'
        )
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'order': {'required': False},
            'initial_duration': {'required': False},
        }
