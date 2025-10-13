from rest_framework import generics, permissions
from .models import Task, TaskList
from .serializers import TaskSerializer
from django.shortcuts import render


class MyTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        task_list = TaskList.objects.filter(owner=user).first()

        if not task_list:
            task_list = TaskList.objects.create(name="Default", owner=user)

        serializer.save(
            assigned_to=user,
            task_list=task_list
        )

class TaskCompleteView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed = True
        task.save()
        return self.retrieve(request, *args, **kwargs)
    


def index(request):
    return render(request, 'index.html')