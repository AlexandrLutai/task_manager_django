# Система управления задачами - Docker Documentation

## 🐳 Описание Docker инфраструктуры

Проект использует Docker для контейнеризации и состоит из следующих сервисов:

### 📦 Сервисы

1. **Redis** - Брокер сообщений и канальный слой
   - Порт: 6379
   - Используется для Celery и Django Channels

2. **Web (Django)** - Основное веб-приложение
   - Порт: 8000
   - REST API и веб-интерфейс
   - WebSocket поддержка

3. **Celery Worker** - Обработчик фоновых задач
   - Отправка уведомлений в Telegram
   - Проверка просроченных задач

4. **Celery Beat** - Планировщик периодических задач
   - Запуск задач по расписанию

5. **Bot** - Telegram бот
   - Интеграция с пользователями через Telegram

## 🚀 Быстрый запуск

### Предварительные требования
- Docker
- Docker Compose
- Telegram Bot Token (получите у @BotFather)

### Запуск

1. **Клонируйте проект и перейдите в директорию:**
   ```bash
   cd task_manager_django
   ```

2. **Настройте environment переменные:**
   ```bash
   cp .env.example .env
   # Отредактируйте .env файл, добавьте ваш BOT_TOKEN
   ```

3. **Запустите все сервисы:**
   ```bash
   ./start.sh up
   ```

   Или вручную:
   ```bash
   docker-compose up -d
   ```

## 🛠 Управление

### Использование скрипта start.sh

```bash
./start.sh [команда]
```

**Доступные команды:**
- `build` - Собрать Docker образы
- `up` - Запустить все сервисы
- `down` - Остановить все сервисы  
- `logs` - Показать логи всех сервисов
- `restart` - Перезапустить все сервисы
- `clean` - Очистить все Docker данные
- `help` - Показать справку

### Прямое использование docker-compose

```bash
# Запуск в фоне
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f web
docker-compose logs -f bot

# Остановка
docker-compose down

# Перестроение образов
docker-compose build

# Запуск с перестройкой
docker-compose up --build
```

## 🔧 Разработка

### Подключение к контейнерам

```bash
# Django shell
docker-compose exec web python manage.py shell

# Bash в web контейнере
docker-compose exec web bash

# Проверка статуса Celery
docker-compose exec celery celery -A config inspect active
```

### Миграции базы данных

```bash
# Создание миграций
docker-compose exec web python manage.py makemigrations

# Применение миграций
docker-compose exec web python manage.py migrate
```

### Создание суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

## 📁 Структура файлов

```
task_manager_django/
├── Dockerfile              # Образ для Django приложения
├── docker-compose.yml      # Конфигурация всех сервисов
├── .dockerignore           # Исключения для Docker build
├── .env.example            # Пример переменных окружения
├── start.sh               # Скрипт управления Docker
├── bot/
│   └── bot.py             # Telegram бот
├── config/                # Django настройки
├── tasks/                 # Основное приложение
└── static/                # Статические файлы
```

## 🔧 Конфигурация

### Environment переменные (.env файл)

```env
# Telegram Bot Token
BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Django настройки
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Redis/Celery (обычно не нужно менять)
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
DJANGO_API=http://web:8000/api/
```

### Dockerfile особенности

- Базовый образ: `python:3.11-slim`
- Установка системных зависимостей
- Создание непривилегированного пользователя
- Копирование кода и установка Python пакетов
- Порт 8000 для Django

## 🌐 Доступ к сервисам

После запуска сервисы доступны по следующим адресам:

- **Веб-приложение**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/
- **Redis**: localhost:6379

## 🐛 Отладка

### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f web
docker-compose logs -f bot
docker-compose logs -f celery
```

### Проверка статуса сервисов

```bash
# Статус контейнеров
docker-compose ps

# Использование ресурсов
docker stats
```

### Перезапуск проблемного сервиса

```bash
# Только бот
docker-compose restart bot

# Только web сервер
docker-compose restart web
```

## 📊 Мониторинг

### Celery мониторинг

```bash
# Активные задачи
docker-compose exec celery celery -A config inspect active

# Статистика
docker-compose exec celery celery -A config inspect stats

# Зарегистрированные задачи
docker-compose exec celery celery -A config inspect registered
```

### Redis мониторинг

```bash
# Подключение к Redis CLI
docker-compose exec redis redis-cli

# Внутри Redis CLI:
# INFO        - Информация о сервере
# KEYS *      - Все ключи
# MONITOR     - Мониторинг команд в реальном времени
```

## 🚀 Production развертывание

Для продакшена рекомендуется:

1. Использовать PostgreSQL вместо SQLite
2. Настроить nginx как reverse proxy
3. Использовать gunicorn вместо runserver
4. Настроить SSL сертификаты
5. Использовать внешний Redis кластер
6. Настроить мониторинг и логирование