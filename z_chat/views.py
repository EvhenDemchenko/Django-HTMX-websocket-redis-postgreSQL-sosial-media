from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView , View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Chat, ChatMessage
from .forms import ChatMessageForm, GroupChatForm , ChatEditForm
from django.http import Http404, HttpResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class ChatView(LoginRequiredMixin, View):
    template_name = 'chat/chat.html'
    form_class = ChatMessageForm

    def get(self, request, *args, **kwargs):
        self.chat_name = self.kwargs.get('chat_name' , 'public-chat')

        self.chat = get_object_or_404(Chat , chat_name = self.chat_name)

        other_user = None

        if self.chat.group_chat_name:
            self.chat_messages = self.chat.messages.all().reverse()[:30]

        elif self.chat.is_private:
            self.chat_messages = self.chat.messages.all().reverse()[:30]

        else:
            self.chat_messages = self.chat.messages.all().order_by('-created')[:30][::-1]
        
        if self.chat.is_private:
            if request.user not in self.chat.members.all():
                raise Http404()
            for member in self.chat.members.all():
                if member != request.user:
                    other_user = member
                    break

        if self.chat.group_chat_name:
            if request.user not in self.chat.members.all():
                self.chat.members.add(request.user)
        
        context = {
            'chat_messages': self.chat_messages,
            'form':self.form_class,
            'chat_name':self.chat_name,
            'chat':self.chat,
        }

        return render(request, 'chat/chat.html', context)

    def post(self, request, *args, **kwargs):
        form = ChatMessageForm()

        if request.htmx:
            form = ChatMessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user
                message.chat = self.chat
                message.save()

                context = {
                    'message':message,
                    'user':request.user
                }
                return render(request, 'chat/partials/chat_message.html' , context)


class GetOrCreatePrivateChat(LoginRequiredMixin , View):
    template_name = 'users/profile_page.html'
    user_model = User

    def get(self,request, *args , **kwargs):
        username = self.kwargs.get('username')

        if request.user.username == username:
            return redirect('chat:home')
        
        other_user = get_object_or_404(User , username=username)
        my_chats =  request.user.member_in_chat.filter(is_private=True)

        if my_chats.exists():
            for my_chat in my_chats:
                if other_user in my_chat.members.all():
                    return redirect('chat:chat-room' , chat_name=my_chat.chat_name)
        
        chat = Chat.objects.create(is_private=True)
        chat.members.add(request.user, other_user)
        return redirect('chat:chat-room' , chat_name=chat.chat_name)
        
class CreateGroupChat( LoginRequiredMixin, CreateView):
    form_class = GroupChatForm
    template_name = 'chat/create_group_chat.html'
    chat_model = Chat

    def form_valid(self, form):
        chat_name = self.request.POST.get('group_chat_name')
        chat_exists = self.chat_model.objects.filter(group_chat_name=chat_name).exclude(
                Q(is_private='True')|
                Q(chat_name='public-chat')|
                Q(chat_name='online-status')
            )

        if chat_exists.exists():
            return redirect('chat:chat-room' , chat_name=chat_exists[0].chat_name)
        else:
            self.chat = form.save(commit=False)
            self.chat.admin = self.request.user
            self.chat.save()
            self.chat.members.add(self.request.user)
            self.chat.save()
            return super().form_valid(form)
    
    def get_success_url(self):
        chat_name = self.chat.chat_name
        return reverse_lazy('chat:chat-room', kwargs={"chat_name":chat_name})


class ChatDelete(UserPassesTestMixin, LoginRequiredMixin , DeleteView):
    chat_model = Chat
    template_name = 'chat/chat_delete.html'
    context_object_name = 'chat'

    def get_object(self , queryset = None):
        chat_name = self.kwargs.get('chat_name')
        chat = get_object_or_404(self.chat_model, chat_name=chat_name)
        return chat

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('chat:home')

    def test_func(self):
        current_chat = self.get_object()
        current_user = self.request.user
        return current_chat.admin == current_user


class ChatEdit(UserPassesTestMixin, LoginRequiredMixin , UpdateView):
    chat_model = Chat
    template_name = 'chat/chat_edit.html'
    context_object_name = 'chat'
    form_class = ChatEditForm

    def get_object(self, queryset =None):
        chat_name = self.kwargs.get('chat_name')
        current_chat = get_object_or_404(self.chat_model , chat_name=chat_name)
        return current_chat
    
    def post(self, request, *args, **kwargs):
        chat = self.get_object()

        form = ChatEditForm(request.POST , instance=chat)
        if form.is_valid():
            members = request.POST.getlist('members')
            form.save()
            for member_id in members:
                member_user = User.objects.get(id=member_id)
                chat.members.remove(member_user)

            return redirect('chat:chat-room', chat_name=chat.chat_name)

    def test_func(self):
        current_chat = self.get_object()
        current_user = self.request.user
        return current_chat.admin == current_user


@login_required
def chat_leave_view(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    chat.members.remove(request.user)
    return redirect('chat:home')


class ChatFileUpload(LoginRequiredMixin , View):
    chat_message_model = ChatMessage
    def post(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat , chat_name = self.kwargs.get('chat_name'))
        if request.htmx and request.FILES:
            image = request.FILES['image']

            message = self.chat_message_model.objects.create(
                chat=chat,
                author=request.user,
                image=image,
            )

            cnannel_layer = get_channel_layer()
            event={
                'type':'chat_message_handler',
                'message_id':message.id,
            }
            async_to_sync(cnannel_layer.group_send)(
                chat.chat_name , event
            )
        return HttpResponse()

# def chat_view(request, chat_name = 'public-chat'):
    # chat = get_object_or_404(Chat , chat_name = chat_name)

    # other_user = None

    # if chat.group_chat_name:
    #     chat_messages = chat.messages.all().reverse()[:30]
    # elif chat.is_private:
    #     chat_messages = chat.messages.all().reverse()[:30]
    # else:
    #     chat_messages = chat.messages.all().reverse()[:30]
    
    # if chat.is_private:
    #     if request.user not in chat.members.all():
    #         raise Http404()
    #     for member in chat.members.all():
    #         if member != request.user:
    #             other_user = member
    #             break

    # if chat.group_chat_name:
    #     if request.user not in chat.members.all():
    #         chat.members.add(request.user)

    # form = ChatMessageForm()

    # if request.htmx:
    #     form = ChatMessageForm(request.POST)
    #     if form.is_valid():
    #         message = form.save(commit=False)
    #         message.author = request.user
    #         message.chat = chat
    #         message.save()

    #         context = {
    #             'message':message,
    #             'user':request.user
    #         }
    #         return render(request, 'chat/partials/chat_message.html' , context)
        
    # context = {
    #     'chat_messages': chat_messages,
    #     'form':form,
    #     'chat_name':chat_name,
    #     'chat':chat,
    # }

    # return render(request, 'chat/chat.html', context)

# def chat_edit_view(request, chat_name):
#     chat = get_object_or_404(Chat, chat_name=chat_name)
#     form = ChatEditForm(instance=chat)

#     if request.method == "POST":
#         form = ChatEditForm(request.POST , instance=chat)
#         if form.is_valid():
#             members = request.POST.getlist('members')
#             form.save()
#             for member_id in members:
#                 member_user = User.objects.get(id=member_id)
#                 chat.members.remove(member_user)

#             return redirect('chat:chat-room', chat_name=chat.chat_name)

#     context = {
#         'form':form,
#         'chat':chat
#     }

#     return render (request, 'chat/chat_edit.html' , context)


# def chat_delete_view(request, chat_name):
#     chat = get_object_or_404(Chat , chat_name=chat_name)

#     if request.method == "POST":
#         if request.user == chat.admin:
#             chat.delete()
#             return redirect('chat:home')
#     context = {'chat' : chat}

#     return render(request, 'chat/chat_delete.html', context)

# def get_or_create_chat(request , username):
#     if request.user.username == username:
#         return redirect('chat:home')
        
#     other_user = get_object_or_404(User , username=username)
#     my_chats =  request.user.member_in_chat.filter(is_private=True)

#     if my_chats.exists():
#         for my_chat in my_chats:
#             if other_user in my_chat.members.all():
#                 return redirect('chat:chat-room' , chat_name=my_chat.chat_name)
#     else:
#         chat = Chat.objects.create(is_private=True)
#         chat.members.add(request.user, other_user)
#         return redirect('chat:chat-room' , chat_name=chat.chat_name)
    

# def create_group_chat_view(request):
#     form = GroupChatForm()
    
#     if request.method == "POST":

#         group_chat_name = request.POST.get('group_chat_name')
#         chat_exists = Chat.objects.filter(group_chat_name=group_chat_name)

#         if chat_exists.exists():
#             return redirect('chat:chat-room' , chat_name = chat_exists[0].chat_name)

#         form = GroupChatForm(request.POST)
#         if form.is_valid():
#             chat = form.save(commit=False)
#             chat.admin = request.user
#             chat.save()
#             chat.members.add(request.user)
#             chat.save()
#             return redirect('chat:chat-room' , chat_name = chat.chat_name)

#     context = {'form':form}

#     return render(request , 'chat/create_group_chat.html' , context)

