"""
WebSocket потребители для приложения управления задачами.

Этот модуль содержит WebSocket потребители для обеспечения связи в реальном времени
между сервером и клиентами. Используется Django Channels для отправки уведомлений
об обновлениях задач всем подключенным пользователям.
"""

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class TaskConsumer(AsyncWebsocketConsumer):
    """
    WebSocket потребитель для обработки обновлений задач в реальном времени.
    
    Этот класс управляет WebSocket соединениями клиентов и обеспечивает
    рассылку уведомлений об изменениях задач всем подключенным пользователям.
    Клиенты автоматически получают обновления когда задачи создаются, 
    изменяются или удаляются.
    """
    
    async def connect(self):
        """
        Обрабатывает новое WebSocket соединение.
        
        Добавляет клиента в группу "tasks" для получения уведомлений
        и принимает WebSocket соединение.
        """
        await self.channel_layer.group_add("tasks", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        Обрабатывает отключение WebSocket соединения.
        
        Удаляет клиента из группы "tasks" при отключении.
        
        Args:
            close_code: Код причины закрытия соединения
        """
        await self.channel_layer.group_discard("tasks", self.channel_name)

    async def send_task_update(self, event):
        """
        Отправляет обновление о задачах клиенту.
        
        Этот метод вызывается когда в группу "tasks" отправляется
        сообщение о обновлении задач. Пересылает данные клиенту
        в JSON формате.
        
        Args:
            event (dict): Событие с данными для отправки клиенту
        """
        await self.send(text_data=json.dumps(event["data"]))