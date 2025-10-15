"""
Конфигурация Django приложения для управления задачами.

Этот модуль определяет настройки приложения 'tasks', которое является
основным компонентом системы управления задачами.
"""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """
    Конфигурационный класс для приложения задач.
    
    Определяет настройки Django приложения, включая тип автополя
    по умолчанию и имя приложения.
    
    Attributes:
        default_auto_field: Тип первичного ключа по умолчанию
        name: Имя приложения Django
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
