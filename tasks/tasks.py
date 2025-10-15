# tasks/tasks.py

from celery import shared_task
import requests
from .models import Task, TelegramProfile

@shared_task
def send_new_task_notification(user_id, task_id):
    try:
        profile = TelegramProfile.objects.get(user_id=user_id)
        task = Task.objects.get(id=task_id)

        message = f"🔔 Вам назначена новая задача: {task.title}"
        requests.get(
            f"https://api.telegram.org/bot<ТВОЙ_ТОКЕН>/sendMessage",
            params={"chat_id": profile.telegram_id, "text": message}
        )
    except Exception as e:
        print("❌ Ошибка отправки:", e)