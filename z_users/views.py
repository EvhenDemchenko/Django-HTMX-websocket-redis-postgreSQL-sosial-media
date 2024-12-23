
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from .models import UserNotification
from django.shortcuts import  redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from z_users.models import Profile
from z_users.forms import ProfileForm, EmailForm
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.




class UserProfile(LoginRequiredMixin,DetailView):
    profile_model = Profile
    context_object_name = 'profile'
    template_name = 'users/profile_page.html'
    
    def get_object(self, queryset = False):
        current_profile = self.profile_model.objects.get(user__username=self.kwargs.get("username"))
        return current_profile
    
    
class UserProfileEdit(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = "users/profile_edit_page.html"
    form_class = ProfileForm
    model = Profile

    def test_func(self):
        return self.request.user == self.get_object().user
    
    def get_object(self, queryset = False):
        current_profile = self.model.objects.get(user=self.request.user) 
        return current_profile
    
    def get_success_url(self):
        return reverse_lazy('users:profile' , kwargs={'username':self.request.user.username})
    

class UserProfileEditEmail(LoginRequiredMixin, View):
    template_name = "users/profile_page.html"
    form_class = EmailForm
    user_model = User


    def post(self,request, *args, **kwargs):
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            email = form.cleaned_data['email']

            if self.user_model.objects.filter(email=email).exclude(id=request.user.id).exists():
                return redirect('users:profile-edit')
            form.save()
        return redirect('users:profile' , username=request.user.username)
    
    def get(self, request, *args, **kwargs):
         if request.htmx:
            form = EmailForm(instance=request.user)
            return render(request, 'partials/email_form.html' , {'form':form})


class ClearNotifications(LoginRequiredMixin, View):
    user_notification_model = UserNotification

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        user_notifications = self.user_notification_model.objects.filter(
            Q(receiver=user)|
            Q(has_seen=False)
        )
        

        for notification in user_notifications:
            notification.has_seen = True
            notification.save()

        return redirect(request.META.get('HTTP_REFERER'))


class ClearCurrentNotification(LoginRequiredMixin, View):
    notification_model = UserNotification
    
    def get(self,request, *args, **kwargs):
        notification_id = self.kwargs['notification_id']
        self.current_notification = self.notification_model.objects.get(id=notification_id)
        self.current_notification.has_seen = True
        self.current_notification.save()
        return redirect('posts:post-info', post_id = self.current_notification.post.id)
    
    def test_func(self):
        return self.request.user == self.current_notification.receiver
    
    
# @login_required
# def user_profile_view(request, username=None):

#     if username:
#         profile = get_object_or_404(User , username=username).profile
#         context = { 'profile':profile}
#     else:
#         profile = Profile.objects.get(user__username=request.user.username)
#         context = { 'profile':profile }

#     return render(request, "users/profile_page.html", context)




# def user_profile_edit_view(request):

#     form = ProfileForm(instance=request.user.profile)
#     profile = get_object_or_404( Profile , user = request.user) 

#     if request.method == "POST":
#         form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid():
#             form.save()

#         context = {"form": form , 'profile':profile}
#         return redirect("users:profile")


#     context = {"form": form, 'profile':profile}
#     return render(request, "users/profile_edit_page.html", context)


#def user_profile_edit_email_view(request):
#     if request.htmx:
#         form  = EmailForm(instance=request.user)
#         return render(request , 'partials/email_form.html' , {'form':form})
    
#     if request.method == "POST":
#         form = EmailForm(request.POST, instance=request.user)

#         if form.is_valid():
#             email = form.cleaned_data['email']

#             if User.objects.filter(email=email).exclude(id=request.user.id).exists():
#                 return redirect('users:profile-edit')
#             form.save()
#         return redirect('users:profile')

#     return redirect('home:feed-page')