from django.http import Http404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status, viewsets

from datetime import datetime, timedelta

from .models import Task as TaskModel
from .models import TaskState as TaskStateModel
from .models import Duration
from .serializers import TaskSerializer
from .serializers import TaskUpdateSerializer
from django.contrib.auth.models import User


# Create your views here.

class Task(viewsets.ViewSet):
    def get_object(self, pk):
        try:
            return TaskModel.objects.get(Q(pk=pk), ~Q(status=1))
        except TaskModel.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            task = self.get_object(pk)
            serializer = TaskSerializer(task)
        else:
            task = TaskModel.objects.filter(~Q(status=1)).order_by('-id')
            serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)

    def get_last_wek(self, request):
        current_date = datetime.now()
        week_date = current_date - timedelta(days=7).order_by('id')
        task = TaskModel.objects.filter(create_date__lte=current_date, create_date__gte=week_date)
        serializer = TaskUpdateSerializer(task, many=True)
        return Response(serializer.data)

    # Filter for get the complete task
    def get_complete(self, request):
        task = TaskModel.objects.filter(status=3).order_by('-id')
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)

    # Filter for get the pending task
    def get_pending(self, request):
        duration = request.query_params.get('duration', None)
        task = TaskModel.objects.filter(
            ~Q(status=1) & ~Q(status=3),
            duration__id=duration
        ).order_by('-create_date')
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)

    # Get the minutes to save them in the database
    def get_minutes(self, timeString):
        time1 = datetime.strptime(timeString, '%H:%M:%S')
        time2 = datetime(1900,1,1)
        return (time1-time2).total_seconds() / 60.0

    # Based on the initial duration saves the type of task
    def get_duration(self):
        durations_objects = Duration.objects.all()
        initial_duration = self.get_minutes(self.request.data.get("initial_duration"))
        for duration_object in durations_objects:
            if duration_object.initial_range <= initial_duration <= duration_object.final_range:
                return duration_object.id

    # Instance of User
    def before_create(self, serializer):
        duration = self.get_duration()
        user = self.request.data.get("user")
        if serializer.is_valid():
            serializer.save(
                user=User.objects.get(pk=user),
                duration=Duration.objects.get(pk=duration)
            )

    # Create the task
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        self.before_create(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update the task
    def put(self, request):
        pk = self.request.data.get("id")
        task = self.get_object(pk)
        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save(duration=Duration.objects.get(pk=self.get_duration()))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def stop(self, request):
        pk = self.request.data.get("id")
        task = self.get_object(pk)
        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save(status=TaskStateModel.objects.get(pk=2))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def finalize(self, request):
        pk = self.request.data.get("id")
        task = self.get_object(pk)
        request.data["final_date"] = datetime.now().strftime('%Y/%m/%d')
        final_duration = self.get_minutes(task.initial_duration) - self.get_minutes(request.data["time_left"])
        request.data["final_duration"] = str(timedelta(minutes=final_duration))
        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save(status=TaskStateModel.objects.get(pk=3))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Change the status of task to "eliminada"
    def delete(self, request):
        pk = self.request.data.get("id")
        task = self.get_object(pk)
        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save(status=TaskStateModel.objects.get(pk=1))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
