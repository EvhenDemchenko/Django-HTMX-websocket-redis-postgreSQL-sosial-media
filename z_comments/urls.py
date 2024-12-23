from django.urls import path
from .views import *

app_name = 'comments'

urlpatterns = [
    # path('post/<int:post_id>/comment-create/', CommentCreate.as_view(), name='comment-create'),
    path('post/<int:post_id>/comment/<int:comment_id>/comment-like/', CommentLike.as_view(), name='comment-like'),
]
