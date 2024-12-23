
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import UserNotification
from z_posts.models import Post
from z_comments.models import Comment

from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
import json


class CommentConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post = get_object_or_404(Post , id = self.post_id)

        async_to_sync(self.channel_layer.group_add)(
            self.post_id, self.channel_name
        )

        self.accept()

    def disconnect(self, code):

        async_to_sync(self.channel_layer.group_discard)(
            self.post_id, self.channel_name
    )


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        comment = Comment.objects.create(
            post = self.post,
            author = self.user,
            body = body,
            )
        
        if self.user != self.post.author:
            UserNotification.objects.create(
                author = self.user,
                receiver = self.post.author,
                post = self.post,
                body = f'{self.user} commented on your post'
            )

        event = {
            'type': 'comment_handler',
            'comment_id':comment.id
        }

        async_to_sync(self.channel_layer.group_send)(
            self.post_id , event
        )

    def comment_handler(self , event):
        comment_id = event['comment_id']
        comment = Comment.objects.get(id=comment_id)
        

        context ={
            'comment':comment,
            'user':self.user,
        }

        html = render_to_string('partials/comment_wrapper.html',context=context)
        self.send(text_data=html)


class UserNotificationsConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'notifications'
        self.user = self.scope['user']
        

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        # self.send_default_notification()
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def user_notification_handler(self, event):
        notification_id = event['notification']
        notification = UserNotification.objects.get(id=notification_id)
        user_notifications = UserNotification.objects.filter(receiver=self.user).exclude(has_seen=True)
        context ={
            'notification':notification,
            'user':self.user,
            'user_notifications':user_notifications
        }

        html = render_to_string('users/notifications.html',context=context)
        self.send(text_data=html)

    