import os
from django.db import models
from django.contrib.auth.models import User
import shortuuid
from cloudinary.models import CloudinaryField

# Create your models here.
class Chat(models.Model):
    chat_name = models.CharField(max_length=128 , unique=True, blank=True)
    users_online = models.ManyToManyField(User , related_name='online_chat' , blank=True )
    members = models.ManyToManyField(User , related_name="member_in_chat", blank=True)
    group_chat_name = models.CharField(max_length=128 , blank=True , null=True)
    is_private = models.BooleanField(default=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE , related_name="admin_in_chat", blank=True, null=True)

    def __str__(self):
        if self.group_chat_name:
            return f'{self.group_chat_name}'
        elif self.is_private:
            return f'{self.members.all()[0].username} --- {self.members.all()[1].username}'
        else:
            return self.chat_name
        
    def save(self, *args, **kwargs):
        if not self.chat_name:
            self.chat_name = shortuuid.uuid()
        super().save(*args, **kwargs)
    
class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat , on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=256 , blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField("image" , blank=True , null=True , resource_type="auto")

    def __str__(self):
        return f'{self.author}: {self.body}'
        
    
    @property
    def is_image(self):
        if self.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp')):
            return True
        else:
            return False

    class Meta:
        ...
        # ordering = ['-created']