from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('', include('z_home.urls' , namespace='home')),
    path('posts/', include('z_posts.urls' , namespace='posts')),
    path('users/', include('z_users.urls' , namespace='users')),
    path('chat/', include('z_chat.urls', namespace='chat')),
    path('comments/' , include('z_comments.urls' , namespace='comments')),
    path('video/' , include('z_videochat.urls' , namespace='videochat')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)