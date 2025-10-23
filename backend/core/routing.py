from django.urls import re_path
from .websocket import TaskConsumer

# Configurazione routing WebSocket per comunicazione real-time
websocket_urlpatterns = [
    re_path(r'^ws/tasks/(?P<task_id>\d+)/$', TaskConsumer.as_asgi()),
]


