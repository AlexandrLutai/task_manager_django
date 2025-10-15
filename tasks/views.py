from rest_framework import generics, permissions
from .models import Task, TaskList, TelegramProfile
from .serializers import TaskSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_tasks_updated():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "tasks",
        {
            "type": "send_task_update",
            "data": {
                "event": "task_updated",
                "message": "Обновлены задачи",
            }
        }
    )

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
        notify_tasks_updated()

class TaskCompleteView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed = True
        task.save()
        notify_tasks_updated()
        return self.retrieve(request, *args, **kwargs)
        
    
class LinkTelegramView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=400)

        profile, created = TelegramProfile.objects.get_or_create(
            user=request.user,
            defaults={"telegram_id": telegram_id}
        )

        if not created and profile.telegram_id != telegram_id:
            profile.telegram_id = telegram_id
            profile.save()

        return Response({"message": "Telegram-аккаунт привязан!"})


class TelegramTaskList(APIView):
    def get(self, request):
        telegram_id = request.GET.get("telegram_id")
        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=400)

        try:
            profile = TelegramProfile.objects.get(telegram_id=telegram_id)
        except TelegramProfile.DoesNotExist:
            return Response({"error": "User not linked"}, status=404)

        tasks = Task.objects.filter(assigned_to=profile.user)
        serializer = TaskSerializer(tasks, many=True)
        notify_tasks_updated()
        return Response(serializer.data)


class TelegramCompleteTask(APIView):
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        task_id = request.data.get("task_id")

        if not telegram_id or not task_id:
            return Response({"error": "telegram_id and task_id required"}, status=400)

        try:
            profile = TelegramProfile.objects.get(telegram_id=telegram_id)
        except TelegramProfile.DoesNotExist:
            return Response({"error": "User not linked"}, status=404)

        try:
            task = Task.objects.get(id=task_id, assigned_to=profile.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or not yours"}, status=404)

        task.completed = True
        task.save()
        return Response({"message": "Task completed ✅"})
    
def index(request):
    return render(request, 'index.html')