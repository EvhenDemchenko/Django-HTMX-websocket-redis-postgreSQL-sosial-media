from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class VideoChatRoom(models.Model):
    room_name = models.CharField(max_length=200 , unique=True)
    members = models.ManyToManyField(User, related_name='video_rooms', blank=True)

    def __str__(self):
        return self.room_name
    
class RoomMember(models.Model):
    name=models.CharField(max_length=200)
    uid=models.CharField(max_length=200)
    room_name=models.CharField(max_length=200)


    def __str__(self):
        return self.name