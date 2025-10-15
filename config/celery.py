import os
from celery import Celery

# Установка модуля настроек Django по умолчанию для программы 'celery'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создание экземпляра приложения Celery
app = Celery("config")

# Загрузка конфигурации из настроек Django с префиксом CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическое обнаружение задач в зарегистрированных Django приложениях
app.autodiscover_tasks()