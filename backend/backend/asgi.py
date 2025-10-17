import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf import settings
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django_asgi_app = get_asgi_application()
if settings.DEBUG:
    # Serve static files (e.g., Django admin) when running with Uvicorn in DEBUG
    django_asgi_app = ASGIStaticFilesHandler(django_asgi_app)

try:
    from core.routing import websocket_urlpatterns
except Exception:
    websocket_urlpatterns = []

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': URLRouter(websocket_urlpatterns),
})
