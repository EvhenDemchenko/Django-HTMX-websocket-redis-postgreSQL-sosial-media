from django.contrib import admin

from z_chat.models import ChatMessage, Chat

# Register your models here.
admin.site.register(Chat)
admin.site.register(ChatMessage)