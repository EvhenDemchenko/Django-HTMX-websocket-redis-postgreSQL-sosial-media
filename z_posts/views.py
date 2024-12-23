from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, View , ListView

from z_users.models import  UserNotification
from .models import Post
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import PostForm
from z_comments.forms import CommentForm
from z_comments.models import Comment
# Create your views here.


class PostList(ListView):
    paginate_by = 5
    template_name = "posts/post_list.html"
    context_object_name = "posts" 
    allow_empty = True

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        return Post.objects.all()
    

class PostInfo(LoginRequiredMixin, DetailView):
    post_model = Post
    comments_model = Comment
    template_name = "posts/post_info.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_object(self, queryset = None):
        post_id = self.kwargs.get("post_id")
        current_post = self.post_model.objects.get(id=post_id)
        return current_post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context['comments'] = self.get_object().comments.all().order_by('created')
        return context


class PostDelete( LoginRequiredMixin, UserPassesTestMixin , DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("posts:post-feed")
    
    def get_object(self, queryset = False):
        post_id = self.kwargs.get("post_id")
        current_post = self.model.objects.get(id=post_id)
        return current_post
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if isinstance(self.object, self.model):
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        
    def test_func(self):
        post_id = self.kwargs.get("post_id")
        current_post = self.model.objects.get(id=post_id)
        return self.request.user == current_post.author


class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post 
    form_class = PostForm
    template_name = "posts/post_edit.html"
    
    def get_object(self, queryset = False):
        post_id = self.kwargs.get("post_id")
        current_post = self.model.objects.get(id=post_id)
        return current_post
    
    def get_success_url(self):
        return reverse_lazy('posts:post-info', kwargs = {'post_id': self.kwargs.get('post_id')})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
        

class PostCreate(LoginRequiredMixin , CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_create.html"


    def get_success_url(self):
        return reverse_lazy('posts:post-info' , kwargs = {'post_id': self.post.id})
    
    def form_valid(self, form):
        self.post = form.save(commit=False)
        self.post.author = self.request.user
        self.post.save()
        return super().form_valid(form)


class PostLike(LoginRequiredMixin , View):
    post_model = Post
    user_notification_model = UserNotification
    def get(self, request, *args, **kwargs):
       
        post_id = self.kwargs.get("post_id")
        current_user = request.user
        current_post = self.post_model.objects.get(id=post_id)


        if current_user in current_post.likes.all():
            current_post.likes.remove(current_user)
            if current_post.author != current_user:
                self.user_notification_model.objects.filter(post = current_post).delete()
        else:       
            current_post.likes.add(current_user)
            if current_post.author != current_user:
                self.user_notification_model.objects.create(
                author = current_user,
                receiver = current_post.author,
                post = current_post,
                body = f'{current_user} liked your post'
        )


        

        if  request.htmx:
            return render(request, "partials/like_count.html" , {'post':current_post})
            
