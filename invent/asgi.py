from django.core.asgi import get_asgi_application
from invent.consumers import NotificationConsumer,UserConsumer
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import os
from .routing import websocket_urlpattern
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invent.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_urlpattern
            )
        ),
})
