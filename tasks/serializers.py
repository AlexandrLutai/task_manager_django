"""
Сериализаторы для REST API приложения управления задачами.

Этот модуль содержит сериализаторы Django REST Framework для преобразования
моделей задач и списков задач в JSON формат и обратно. Используется для
обработки API запросов и ответов.
"""

from rest_framework import serializers
from .models import Task, TaskList


class TaskListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели TaskList.
    
    Преобразует объекты TaskList в JSON формат для REST API.
    Используется для создания, чтения, обновления и удаления
    списков задач через API.
    
    Meta:
        model: Модель TaskList
        fields: Все поля модели включены в сериализацию
    """
    class Meta:
        model = TaskList
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Task.
    
    Преобразует объекты Task в JSON формат для REST API.
    Поля 'assigned_to' и 'task_list' помечены как read-only,
    так как они устанавливаются автоматически в представлениях
    на основе аутентифицированного пользователя.
    
    Meta:
        model: Модель Task
        fields: Все поля модели включены в сериализацию
        read_only_fields: Поля, которые нельзя изменить через API
    """
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('assigned_to', 'task_list')