from django.db import models
from z_posts.models import Post
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User , on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(max_length=128 , blank=False , null=False)
    created = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User , related_name="liked_comments" , blank=True)

    def __str__(self):
        return f"{self.author} - {self.body[:10]}"
    
    class Meta:
        ordering = ['-created']
    
