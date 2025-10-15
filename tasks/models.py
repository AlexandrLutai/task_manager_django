"""
Модели для системы управления задачами.

Этот модуль содержит определения моделей Django для управления задачами,
списками задач и профилями пользователей Telegram.
"""

from django.db import models
from django.contrib.auth.models import User


class TaskList(models.Model):
    """
    Модель списка задач.
    
    Представляет собой контейнер для группировки задач одного пользователя.
    Каждый пользователь может иметь несколько списков задач для организации
    своей работы.
    
    Attributes:
        name (str): Название списка задач (максимум 100 символов)
        owner (User): Владелец списка задач (связь с моделью User)
    """
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Строковое представление списка задач."""
        return self.name


class Task(models.Model):
    """
    Модель задачи.
    
    Представляет отдельную задачу в системе управления задачами.
    Каждая задача принадлежит конкретному списку задач и назначена
    определенному пользователю.
    
    Attributes:
        title (str): Заголовок задачи (максимум 255 символов)
        description (str): Описание задачи (может быть пустым)
        deadline (datetime): Срок выполнения задачи
        completed (bool): Флаг выполнения задачи (по умолчанию False)
        task_list (TaskList): Список задач, к которому принадлежит задача
        assigned_to (User): Пользователь, которому назначена задача
        created_at (datetime): Время создания задачи (автоматически)
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    completed = models.BooleanField(default=False)

    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Строковое представление задачи."""
        return f'{self.title} ({self.assigned_to.username})'


class TelegramProfile(models.Model):
    """
    Модель профиля пользователя Telegram.
    
    Связывает учетную запись пользователя Django с его аккаунтом Telegram
    для интеграции с Telegram ботом. Позволяет отправлять уведомления
    и управлять задачами через Telegram.
    
    Attributes:
        user (User): Связанный пользователь Django (one-to-one связь)
        telegram_id (int): Уникальный ID пользователя в Telegram
        jwt_token (str): JWT токен для аутентификации (может быть пустым)
        created_at (datetime): Время создания профиля (автоматически)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.BigIntegerField(unique=True)
    jwt_token = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Строковое представление профиля Telegram."""
        return f'Telegram профиль {self.user.username} (ID: {self.telegram_id})'