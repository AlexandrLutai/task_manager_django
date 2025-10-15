# Task Manager Django

Система управления задачами с интеграцией Telegram и поддержкой фоновых задач через Celery.

## 🚀 Реализовано

- **REST API** для управления задачами (создание, просмотр, завершение)
- **JWT аутентификация** пользователей
- **Веб-интерфейс** (главная страница)
- **Интеграция с Telegram ботом**:
  - Получение и завершение задач через Telegram
  - Привязка Telegram аккаунта к пользователю
- **WebSocket** уведомления о событиях (Django Channels)
- **Celery** для фоновых задач:
  - Уведомления о просроченных задачах
  - Уведомления о новых задачах
- **Docker** и **docker-compose** для быстрой сборки и запуска всех сервисов
- **Админ-панель Django** для управления пользователями и задачами

## 🛠 Как запустить проект

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/AlexandrLutai/task_manager_django.git
cd task_manager_django
```

### 2. Настройте переменные окружения
```bash
cp .env.example .env
# Откройте .env и укажите свои токены Telegram и секрет Django
```

### 3. Запустите проект через Docker Compose
```bash
./start.sh up
```
или вручную:
```bash
docker-compose up -d
```

- Веб-интерфейс: http://localhost:8000
- Django Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/

### 4. Управление сервисами

- Остановить:
  ```bash
  ./start.sh down
  ```
- Логи:
  ```bash
  ./start.sh logs
  ```
- Перезапустить:
  ```bash
  ./start.sh restart
  ```

### 5. Создать суперпользователя
```bash
docker-compose exec web python manage.py createsuperuser
```

## 📱 Интеграция с Telegram
- Получите токен у @BotFather и укажите его в .env
- После запуска бота используйте команды /start, /tasks, /complete_X, /login

## 📝 Стек технологий
- Python 3.11, Django, Django REST Framework
- Celery, Redis
- aiogram (Telegram Bot)
- Docker, docker-compose
- SQLite (по умолчанию, можно заменить на PostgreSQL)

## 📦 Структура
```
task_manager_django/
├── bot/           # Telegram бот
├── config/        # Django настройки
├── tasks/         # Основное приложение
├── static/        # Статика
├── templates/     # Шаблоны
├── Dockerfile
├── docker-compose.yml
├── start.sh
├── .env.example
└── ...
```

## ℹ️ Дополнительно
- Подробная документация по Docker: см. `DOCKER_README.md`
- Для продакшена рекомендуется использовать PostgreSQL, nginx, gunicorn
