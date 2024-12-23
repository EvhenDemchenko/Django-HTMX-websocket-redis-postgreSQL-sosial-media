
from django import forms
from django.forms import widgets
from .models import ChatMessage , Chat
from cloudinary.forms import CloudinaryFileField

class ChatMessageForm(forms.ModelForm):
    body = forms.CharField(max_length=256 , widget=forms.TextInput(attrs={ "placeholder":"Write your message!" ,"class":"w-full focus:outline-none focus:placeholder-gray-400 text-gray-600 placeholder-gray-600 pl-12 bg-gray-200 rounded-md py-3",'autofocus':True }))
    image = CloudinaryFileField('image')
    class Meta:
        model = ChatMessage
        fields = ['body','image']


class GroupChatForm(forms.ModelForm):
    group_chat_name = forms.CharField(max_length=256 , widget=forms.TextInput(attrs={ 'type':'text' ,'name':"message", "placeholder":"Type your chat name...", "class":"w-full px-4 py-2 rounded-lg border border-gray-200 focus:outline-none" ,'autofocus':True }))

    class Meta:
        model = Chat
        fields = ['group_chat_name']


class ChatEditForm(forms.ModelForm):
    group_chat_name = forms.CharField(max_length=128 , widget=forms.TextInput(attrs={ 'type':'text' ,'name':"message", "placeholder":"Type your chat name...", "class":"w-full px-4 py-2 rounded-lg border border-gray-200 focus:outline-none" }))
    class Meta:
        model = Chat
        fields = ['group_chat_name']