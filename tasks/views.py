"""
Представления (views) для приложения управления задачами.

Этот модуль содержит API представления для работы с задачами через REST API,
интеграцию с Telegram ботом и веб-интерфейс. Включает функциональность для
создания, просмотра и обновления задач, а также для связи аккаунтов с Telegram.
"""

from rest_framework import generics, permissions
from .models import Task, TaskList, TelegramProfile
from .serializers import TaskSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .tasks import send_new_task_notification


def notify_tasks_updated():
    """
    Отправляет уведомление о обновлении задач через WebSocket.
    
    Функция использует Django Channels для отправки сообщения всем подключенным
    клиентам в группе "tasks" о том, что список задач был обновлен.
    Это позволяет обновлять интерфейс в реальном времени.
    """
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
    """
    Представление для получения списка задач текущего пользователя.
    
    Возвращает только задачи, назначенные аутентифицированному пользователю.
    Используется для отображения персональных задач в веб-интерфейсе.
    
    Attributes:
        serializer_class: Сериализатор для задач
        permission_classes: Требуется аутентификация
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращает задачи, назначенные текущему пользователю."""
        return Task.objects.filter(assigned_to=self.request.user)

class TaskCreateView(generics.CreateAPIView):
    """
    Представление для создания новых задач.
    
    Создает новую задачу для аутентифицированного пользователя.
    Автоматически создает список задач по умолчанию, если у пользователя
    его еще нет. После создания отправляет уведомления через WebSocket
    и планирует отправку уведомления в Telegram.
    
    Attributes:
        serializer_class: Сериализатор для задач
        permission_classes: Требуется аутентификация
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Создает задачу с автоматическим назначением пользователя и списка.
        
        Args:
            serializer: Сериализатор с валидными данными задачи
        """
        user = self.request.user
        task_list = TaskList.objects.filter(owner=user).first()

        if not task_list:
            task_list = TaskList.objects.create(name="Default", owner=user)

        task = serializer.save(
            assigned_to=user,
            task_list=task_list
        )
        notify_tasks_updated()
        send_new_task_notification.delay(user.id, task.id)

class TaskCompleteView(generics.UpdateAPIView):
    """
    Представление для отметки задач как выполненных.
    
    Позволяет пользователям отмечать свои задачи как выполненные
    через PATCH запрос. После обновления отправляет уведомление
    через WebSocket для обновления интерфейса в реальном времени.
    
    Attributes:
        queryset: Все задачи в системе
        serializer_class: Сериализатор для задач
        permission_classes: Требуется аутентификация
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        Отмечает задачу как выполненную.
        
        Args:
            request: HTTP запрос
            *args, **kwargs: Дополнительные аргументы
            
        Returns:
            Response: Обновленные данные задачи
        """
        task = self.get_object()
        task.completed = True
        task.save()
        notify_tasks_updated()
        return self.retrieve(request, *args, **kwargs)
        
    
class LinkTelegramView(APIView):
    """
    API для привязки аккаунта пользователя к Telegram.
    
    Позволяет пользователям связать свой аккаунт в системе с аккаунтом
    в Telegram для получения уведомлений и управления задачами через бота.
    Создает или обновляет профиль Telegram для пользователя.
    
    Attributes:
        permission_classes: Требуется аутентификация
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Привязывает Telegram аккаунт к текущему пользователю.
        
        Args:
            request: HTTP запрос с telegram_id в data
            
        Returns:
            Response: Сообщение о успешной привязке или ошибке
        """
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
    """
    API для получения списка задач через Telegram бота.
    
    Позволяет Telegram боту получать список задач пользователя
    по его Telegram ID. Используется для отображения задач
    непосредственно в Telegram чате.
    """
    
    def get(self, request):
        """
        Возвращает список задач пользователя по Telegram ID.
        
        Args:
            request: HTTP запрос с telegram_id в параметрах
            
        Returns:
            Response: Список задач пользователя или ошибку
        """
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
    """
    API для отметки задач как выполненных через Telegram бота.
    
    Позволяет пользователям отмечать свои задачи как выполненные
    непосредственно из Telegram чата через бота.
    """
    
    def post(self, request):
        """
        Отмечает задачу как выполненную по запросу от Telegram бота.
        
        Args:
            request: HTTP запрос с telegram_id и task_id в data
            
        Returns:
            Response: Сообщение о успешном выполнении или ошибке
        """
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
    """
    Отображает главную страницу веб-приложения.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Рендер главной страницы (index.html)
    """
    return render(request, 'index.html')