import json
import os
import signal
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer


class TaskConsumer(AsyncWebsocketConsumer):
    # Connessione WebSocket
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.group_name = f'task_{self.task_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    # Disconnessione WebSocket
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        # Alla disconnessione del client, interrompe il task se è in corso
        data = await self._interrupt_task_if_running()
        # Opzionale: broadcast finale (potrebbe non esserci nessun listener)
        if data:
            await self.channel_layer.group_send(self.group_name, {
                'type': 'task_update',
                'data': data
            })

    # Gestisce aggiornamenti del task
    async def task_update(self, event):
        await self.send(text_data=json.dumps(event['data']))

    # Interrompe il task se il client si disconnette
    @database_sync_to_async
    def _interrupt_task_if_running(self):
        try:
            task = Task.objects.get(id=self.task_id)
            if task.status in ['running', 'pending']:
                # Prova a terminare il processo se presente
                if task.process_id:
                    try:
                        os.kill(task.process_id, signal.SIGTERM)
                    except Exception:
                        pass
                # Marca come interrotto con messaggio dedicato
                task.status = 'interrupted'
                task.finished_at = timezone.now()
                if task.started_at is not None:
                    task.total_execution_time = task.finished_at - task.started_at
                task.message = 'Task interrotto (disconnessione client).'
                task.save()
                return TaskSerializer(task).data
        except Task.DoesNotExist:
            return None
        return None


