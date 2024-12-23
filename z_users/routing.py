from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/comment/<post_id>", CommentConsumer.as_asgi()),
    path("ws/notifications/", UserNotificationsConsumer.as_asgi()),
]



