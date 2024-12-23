from django.urls import path
from z_posts.views import PostCreate, PostList, PostInfo, PostDelete, PostEdit, PostLike

app_name = 'posts'

urlpatterns = [
    path('post-feed/', PostList.as_view(), name='post-feed'),
    path('post-create/', PostCreate.as_view(), name='post-create'),
    path('post-feed/<int:post_id>/info', PostInfo.as_view(), name='post-info'),
    path('post-feed/<int:post_id>/edit', PostEdit.as_view(), name='post-edit'),
    path('post-feed/<int:post_id>/delete', PostDelete.as_view(), name='post-delete'),
    path('post-feed/<int:post_id>/like', PostLike.as_view(), name='post-like'),
]