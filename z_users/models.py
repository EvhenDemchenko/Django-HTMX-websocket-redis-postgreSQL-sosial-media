from email.policy import default
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from z_posts.models import Post
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE, related_name='profile' )
    # image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True, default='https://res.cloudinary.com/dsnftekpz/image/upload/v1734869367/q8cupwjicmns3t6iyhqp.jpg')
    info = models.CharField(max_length=300, blank=True, null=True)
    displayname = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return f'{self.user}'
    
    @property
    def name(self):
        if self.displayname:
            return f'{self.displayname}'
        else:
            return f'{self.user.username}'
        
    
@receiver(post_save , sender=User)
def create_user_profile(sender , instance , created , **kwargs):
    if created:
        Profile.objects.create(user=instance, displayname=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender , instance , **kwargs):
    instance.profile.save()

from django.db import models
from django.contrib.auth.models import User


class UserNotification(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_comment_notifications")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_notifications")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="+")
    body = models.CharField(max_length=256, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    has_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'from @{self.author} -> to @{self.receiver}'
    