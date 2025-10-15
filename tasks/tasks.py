"""
Celery задачи для системы управления задачами.

Этот модуль содержит фоновые задачи, выполняемые асинхронно с помощью Celery.
Включает функции для проверки просроченных задач и отправки уведомлений
в Telegram.
"""

from celery import shared_task
from .models import Task, TelegramProfile
from django.utils import timezone
import requests
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


@shared_task
def check_expired_tasks():
    """
    Проверяет просроченные задачи и отправляет уведомления в Telegram.
    
    Эта задача предназначена для периодического выполнения (например, через cron).
    Находит все невыполненные задачи с истекшим сроком и отправляет уведомления
    пользователям через Telegram бота, если у них настроена интеграция.
    
    Returns:
        None: Функция не возвращает значения, но может печатать ошибки
    """
    now = timezone.now()
    expired_tasks = Task.objects.filter(completed=False, deadline__lt=now)

    for task in expired_tasks:
        user = task.assigned_to
        try:
            profile = TelegramProfile.objects.get(user=user)
        except TelegramProfile.DoesNotExist:
            continue  # Telegram не привязан — пропускаем

        message = (
            f"⏰ Задача просрочена: <b>{task.title}</b>\n"
            f"Срок: {task.deadline.strftime('%Y-%m-%d %H:%M')}"
        )
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                data={
                    "chat_id": profile.telegram_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
            )
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")


@shared_task
def send_new_task_notification(user_id, task_id):
    """
    Отправляет уведомление о новой задаче в Telegram.
    
    Отправляет пользователю уведомление о создании новой задачи
    через Telegram бота, если у пользователя настроена интеграция.
    
    Args:
        user_id (int): ID пользователя Django
        task_id (int): ID созданной задачи
        
    Returns:
        None: Функция не возвращает значения, но может печатать ошибки
    """
    try:
        task = Task.objects.get(id=task_id)
        profile = TelegramProfile.objects.get(user_id=user_id)
        
        message = (
            f"📋 Новая задача: <b>{task.title}</b>\n"
            f"Описание: {task.description}\n"
            f"Срок: {task.deadline.strftime('%Y-%m-%d %H:%M')}"
        )
        
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={
                "chat_id": profile.telegram_id,
                "text": message,
                "parse_mode": "HTML"
            }
        )
    except (Task.DoesNotExist, TelegramProfile.DoesNotExist):
        print(f"Не удалось найти задачу {task_id} или профиль пользователя {user_id}")
    except Exception as e:
        print(f"Ошибка отправки уведомления о новой задаче: {e}")