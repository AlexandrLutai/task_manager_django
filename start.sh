#!/bin/bash

"""
Скрипт для запуска системы управления задачами в Docker.

Этот скрипт автоматизирует процесс сборки и запуска всех компонентов
системы управления задачами в Docker контейнерах.

Компоненты:
1. Redis - брокер сообщений и канальный слой
2. Django Web - основное приложение с API
3. Celery Worker - обработка фоновых задач
4. Celery Beat - планировщик периодических задач
5. Telegram Bot - интеграция с Telegram

Использование:
    ./start.sh [команда]
    
Команды:
    build   - Собрать Docker образы
    up      - Запустить все сервисы
    down    - Остановить все сервисы
    logs    - Показать логи всех сервисов
    restart - Перезапустить все сервисы
    clean   - Очистить все Docker данные
"""

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода информации
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Функция для вывода предупреждений
warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Функция для вывода ошибок
error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка наличия .env файла
check_env_file() {
    if [ ! -f .env ]; then
        warn ".env файл не найден"
        info "Копирую .env.example в .env"
        cp .env.example .env
        warn "Пожалуйста, отредактируйте .env файл и добавьте ваши токены"
        echo
        cat .env.example
        echo
        read -p "Нажмите Enter после редактирования .env файла..."
    fi
}

# Функция сборки
build() {
    info "Сборка Docker образов..."
    docker-compose build
    info "Сборка завершена!"
}

# Функция запуска
up() {
    check_env_file
    info "Запуск всех сервисов..."
    docker-compose up -d
    info "Все сервисы запущены!"
    info "Веб-приложение доступно по адресу: http://localhost:8000"
    info "Redis доступен по порту: 6379"
}

# Функция остановки
down() {
    info "Остановка всех сервисов..."
    docker-compose down
    info "Все сервисы остановлены!"
}

# Функция просмотра логов
logs() {
    docker-compose logs -f
}

# Функция перезапуска
restart() {
    info "Перезапуск всех сервисов..."
    docker-compose restart
    info "Все сервисы перезапущены!"
}

# Функция очистки
clean() {
    warn "Это удалит все Docker контейнеры, образы и volumes!"
    read -p "Вы уверены? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        info "Остановка и удаление контейнеров..."
        docker-compose down -v --remove-orphans
        info "Удаление образов..."
        docker image prune -f
        info "Очистка завершена!"
    else
        info "Очистка отменена"
    fi
}

# Функция помощи
help() {
    echo "Использование: $0 [команда]"
    echo
    echo "Команды:"
    echo "  build    - Собрать Docker образы"
    echo "  up       - Запустить все сервисы"
    echo "  down     - Остановить все сервисы"
    echo "  logs     - Показать логи всех сервисов"
    echo "  restart  - Перезапустить все сервисы"
    echo "  clean    - Очистить все Docker данные"
    echo "  help     - Показать эту справку"
}

# Основная логика
case "${1:-up}" in
    build)
        build
        ;;
    up)
        up
        ;;
    down)
        down
        ;;
    logs)
        logs
        ;;
    restart)
        restart
        ;;
    clean)
        clean
        ;;
    help|--help|-h)
        help
        ;;
    *)
        error "Неизвестная команда: $1"
        help
        exit 1
        ;;
esac