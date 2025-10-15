"""
URL конфигурация для приложения управления задачами.

Этот файл определяет все API эндпоинты для работы с задачами,
включая веб-интерфейс и интеграцию с Telegram ботом.

URL паттерны:
- my-tasks/ - Получение списка задач пользователя (GET)
- create-task/ - Создание новой задачи (POST)
- complete-task/<id>/ - Отметка задачи как выполненной (PATCH)
- link-telegram/ - Привязка Telegram аккаунта (POST)
- telegram/tasks/ - API для бота: получение задач по Telegram ID (GET)
- telegram/complete-task/ - API для бота: завершение задачи (POST)
- '' - Главная страница с веб-интерфейсом
"""

from django.urls import path
from .views import MyTaskListView, TaskCreateView, TaskCompleteView,index, LinkTelegramView
from .views import TelegramTaskList, TelegramCompleteTask

urlpatterns = [
    path('my-tasks/', MyTaskListView.as_view(), name='my-tasks'),
    path('create-task/', TaskCreateView.as_view(), name='create-task'),
    path('complete-task/<int:pk>/', TaskCompleteView.as_view(), name='complete-task'),
    path('link-telegram/', LinkTelegramView.as_view(), name='link-telegram'),
    path('telegram/tasks/', TelegramTaskList.as_view(), name='telegram-tasks'),
    path('telegram/complete-task/', TelegramCompleteTask.as_view(), name='telegram-complete-task'),
    path('', index)
]