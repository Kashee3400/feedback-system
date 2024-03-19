from invent.consumers import NotificationConsumer,UserConsumer
from django.urls import path


websocket_urlpattern =[
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    path("ws/users/", UserConsumer.as_asgi()),
]