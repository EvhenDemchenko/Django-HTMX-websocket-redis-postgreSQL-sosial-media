from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import Chat, ChatMessage
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
import json

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.user = self.scope['user']
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.chat = get_object_or_404(Chat , chat_name = self.chat_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chat_name, self.channel_name
        )


        if self.user not in self.chat.users_online.all():
            self.chat.users_online.add(self.user)

        self.update_online_count()
        self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name , self.channel_name
        )


        if self.user in self.chat.users_online.all():
            self.chat.users_online.remove(self.user)
            self.update_online_count()


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = ChatMessage.objects.create(
            body = body,
            author = self.user,
            chat = self.chat
        )

        event = {
            'type': 'chat_message_handler',
            'message_id': message.id
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chat_name , event
        )

    def chat_message_handler(self , event):
        message_id = event['message_id']
        message = ChatMessage.objects.get(id=message_id)

        context = {
            'message':message,
            'user':self.user,
        }

        html = render_to_string('chat/partials/chat_message.html',context=context)
        self.send(text_data=html)

    def update_online_count(self):
        # online_users = self.chat.users_online.all()

        event = {
            'type': 'online_count_handler',
            # 'online_users': online_users
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chat_name , event
        )

    def online_count_handler(self , event):
        online_users = self.chat.users_online.all()

        context = {
            'online_users':online_users,
            'user':self.user,
        }
        html = render_to_string('chat/partials/online_in_chat.html', context=context)

        self.send(text_data=html)

class OnlineStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chat_name = 'online-status'
        self.online_status= Chat.objects.get(chat_name = self.chat_name)


        if self.user not in self.online_status.users_online.all():
            self.online_status.users_online.add(self.user)

        async_to_sync(self.channel_layer.group_add)(
            self.chat_name, self.channel_name
        )


        self.online_status_fn()
        self.accept()

    def disconnect(self, code):

        if self.user in self.online_status.users_online.all():
            self.online_status.users_online.remove(self.user)

        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name , self.channel_name
        )

        self.online_status_fn()

        
    def online_status_fn(self ):

        event = {
            'type': 'online_status_handler',
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chat_name , event
        )

    def online_status_handler(self,event):
        online_count = self.online_status.users_online.all().exclude(id=self.user.id).count()


        my_chats = self.user.member_in_chat.all()

        online_users_in_public_chat = Chat.objects.get(chat_name="public-chat").users_online.all().exclude(id=self.user.id)
        
        online_users_in_private_chat = [chat for chat in my_chats.filter(is_private=True) if chat.users_online.all().exclude(id=self.user.id)]

        online_users_in_group_chat = [chat for chat in my_chats.filter(group_chat_name__isnull=False) if chat.users_online.all().exclude(id=self.user.id)]

        online_in_chats = False

        if online_users_in_public_chat or online_users_in_private_chat or online_users_in_group_chat:
            online_in_chats = True


        context = {
                'online_count':online_count,
                'user':self.user,   
                'online_in_chats':online_in_chats,
                }
        
        html = render_to_string('chat/partials/online_status.html',context=context)

        self.send(text_data=html)