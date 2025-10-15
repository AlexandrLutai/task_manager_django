"""
Конфигурация административной панели Django для приложения задач.

Этот модуль регистрирует модели Task и TaskList в административной
панели Django, позволяя администраторам управлять задачами и списками
задач через веб-интерфейс Django Admin.
"""

from django.contrib import admin
from .models import Task, TaskList, TelegramProfile


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели Task.
    
    Определяет отображение задач в админ-панели с удобными
    фильтрами и полями для просмотра.
    """
    list_display = ('title', 'assigned_to', 'deadline', 'completed', 'created_at')
    list_filter = ('completed', 'deadline', 'created_at')
    search_fields = ('title', 'description', 'assigned_to__username')
    date_hierarchy = 'deadline'


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели TaskList.
    
    Определяет отображение списков задач в админ-панели.
    """
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')


@admin.register(TelegramProfile)
class TelegramProfileAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели TelegramProfile.
    
    Определяет отображение профилей Telegram в админ-панели.
    """
    list_display = ('user', 'telegram_id', 'created_at')
    search_fields = ('user__username', 'telegram_id')
    readonly_fields = ('created_at',)