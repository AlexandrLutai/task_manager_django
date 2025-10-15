"""
Telegram бот для системы управления задачами.

Этот модуль содержит Telegram бота, который интегрируется с Django приложением
для управления задачами. Пользователи могут просматривать свои задачи,
отмечать их как выполненные и получать инструкции по привязке аккаунта
непосредственно через Telegram.

Бот использует aiogram для работы с Telegram API и aiohttp для общения
с Django REST API.
"""

import logging
import os
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
DJANGO_API_URL = os.getenv("DJANGO_API", "http://127.0.0.1:8000/api/")

# Инициализация бота
logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    """
    Обработчик команды /start.
    
    Приветствует пользователя и объясняет как использовать бота.
    Показывает инструкции по привязке Telegram аккаунта к веб-приложению.
    
    Args:
        message (Message): Сообщение от пользователя с командой /start
    """
    await message.answer(
        "👋 Привет! Этот бот помогает управлять задачами из веб-приложения.\n\n"
        "Чтобы использовать бота:\n"
        "1️⃣ Авторизуйся в вебе и открой форму привязки Telegram\n"
        f"2️⃣ Введи вот этот код: {message.from_user.id}\n"
        "3️⃣ Потом напиши команду /tasks"
    )


@dp.message(Command("tasks"))
async def tasks(message: Message):
    """
    Обработчик команды /tasks.
    
    Получает и отображает список задач пользователя из Django API.
    Если аккаунт не привязан, показывает инструкции по привязке.
    Для невыполненных задач добавляет кнопки для завершения.
    
    Args:
        message (Message): Сообщение от пользователя с командой /tasks
    """
    telegram_id = message.from_user.id

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{DJANGO_API_URL}telegram/tasks/?telegram_id={telegram_id}"
        ) as resp:
            if resp.status == 200:
                tasks = await resp.json()
                if not tasks:
                    await message.answer("🎉 У тебя пока нет задач!")
                    return

                for task in tasks:
                    text = (
                        f"<b>{task['title']}</b>\n"
                        f"🕓 Срок: {task['deadline']}\n"
                        f"{'✅ Выполнена' if task['completed'] else '❌ Не выполнена'}"
                    )
                    if not task["completed"]:
                        text += f"\n\nЧтобы завершить:\n/complete_{task['id']}"
                    await message.answer(text)
            elif resp.status == 404:
                await message.answer(
                    "🔒 Ты ещё не привязал Telegram к аккаунту.\n\n"
                    "Напиши /login, чтобы получить код и ввести его на сайте."
                )
            else:
                await message.answer("⚠️ Не удалось получить задачи. Попробуй позже.")


@dp.message(lambda m: m.text.startswith("/complete_"))
async def complete_task(message: Message):
    """
    Обработчик команд завершения задач (/complete_X).
    
    Позволяет пользователям отмечать задачи как выполненные
    прямо из Telegram. Извлекает ID задачи из команды и отправляет
    запрос в Django API для обновления статуса задачи.
    
    Args:
        message (Message): Сообщение с командой /complete_X, где X - ID задачи
    """
    telegram_id = message.from_user.id

    try:
        task_id = int(message.text.replace("/complete_", ""))
    except ValueError:
        await message.answer("❌ Неверный формат команды. Пример: /complete_5")
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{DJANGO_API_URL}telegram/complete-task/",
            json={"telegram_id": telegram_id, "task_id": task_id}
        ) as resp:
            if resp.status == 200:
                await message.answer("✅ Задача успешно завершена.")
            elif resp.status == 404:
                await message.answer("❌ Задача не найдена или не твоя.")
            else:
                await message.answer("⚠️ Не удалось завершить задачу.")


@dp.message(Command("login"))
async def login_help(message: Message):
    """
    Обработчик команды /login.
    
    Предоставляет пользователю инструкции по привязке его Telegram аккаунта
    к веб-приложению. Показывает уникальный Telegram ID пользователя,
    который нужно ввести в веб-интерфейсе.
    
    Args:
        message (Message): Сообщение от пользователя с командой /login
    """
    telegram_id = message.from_user.id
    await message.answer(
        f"🔐 Чтобы привязать Telegram к аккаунту:\n\n"
        f"1️⃣ Войдите в веб-приложение\n"
        f"2️⃣ Перейдите в раздел <b>Привязка Telegram</b>\n"
        f"3️⃣ Введите этот код: <code>{telegram_id}</code>\n\n"
        "После привязки используйте команду /tasks"
    )


if __name__ == "__main__":
    """
    Точка входа для запуска Telegram бота.
    
    Запускает поллинг для получения обновлений от Telegram API
    и обработки входящих сообщений.
    """
    import asyncio
    asyncio.run(dp.start_polling(bot))