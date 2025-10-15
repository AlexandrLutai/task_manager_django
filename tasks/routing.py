"""
WebSocket маршрутизация для приложения управления задачами.

Этот модуль определяет WebSocket URL паттерны для Django Channels.
Используется для создания соединений в реальном времени между
клиентами и сервером для получения обновлений о задачах.

WebSocket эндпоинты:
- ws/tasks/ - Подключение к группе задач для получения обновлений
"""

from django.urls import re_path
from .consumers import TaskConsumer

websocket_urlpatterns = [
    re_path(r"ws/tasks/$", TaskConsumer.as_asgi()),
]