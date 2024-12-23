from django.urls import path
from .views import ChatView , GetOrCreatePrivateChat,ChatDelete,ChatEdit,chat_leave_view , CreateGroupChat, ChatFileUpload

app_name = 'chat'

urlpatterns = [
    path('', ChatView.as_view() , name='home'),
    path('new-groupchat/', CreateGroupChat.as_view() , name='new-groupchat'),
    path('<username>' , GetOrCreatePrivateChat.as_view() , name="start-chat"),
    path('room/<chat_name>', ChatView.as_view() , name='chat-room'),
    path('room/<chat_name>/delete', ChatDelete.as_view() , name='chat-delete'),
    path('room/<chat_name>/edit', ChatEdit.as_view() , name='chat-edit'),
    path('room/<chat_id>/leave', chat_leave_view , name='chat-leave'),
    path('room/fileupload/<chat_name>', ChatFileUpload.as_view() , name='chat-file-upload'),
]
