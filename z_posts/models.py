
from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from cloudinary.models import CloudinaryField
# Create your models here.


class Post(models.Model):
    body = CKEditor5Field('body', config_name='extends')
    # image = models.ImageField(upload_to='post_images' ,  null=True , blank=True)
    image = CloudinaryField('image', null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    likes = models.ManyToManyField(User , related_name="liked_posts" , blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author} - {self.body[:15]}'

    class Meta:
        ordering = ['-created']