from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/chat/<chat_name>", ChatConsumer.as_asgi()),
    path("ws/online-status/", OnlineStatusConsumer.as_asgi()),
]



