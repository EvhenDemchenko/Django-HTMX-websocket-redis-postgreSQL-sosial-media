
from django.urls import path
from . import views

app_name = 'videochat'

urlpatterns = [
    path('', views.index, name='index'),
    path('room/', views.room, name='room'),
    path('get_token/', views.get_token, name='get_token'),
    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
]
