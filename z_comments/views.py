from django.shortcuts import render
from .models import Comment
from z_posts.models import Post
from django.views.generic.edit import  UpdateView
from django.views.generic import View 
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# class CommentCreate(CreateView):
#     post_model = Post
#     template_name = 'posts/post_info.html'
#     form_class = CommentForm

#     def form_valid(self, form):
#         self.current_post = self.post_model.objects.get(id=self.kwargs.get("post_id"))
#         if self.request.htmx:                  
#             comment = form.save(commit=False)
#             comment.author = self.request.user
#             comment.post = self.current_post
#             comment.save()
#             return render(self.request,'partials/comment_body.html' , {'comment':comment})
    
    



class CommentLike( LoginRequiredMixin, UpdateView):
    comment_model = Comment 
    template_name = 'posts/post_info.html'
    post_model = Post

    def get(self, request, *args, **kwargs):
        if request.htmx:
            comment_id = self.kwargs.get("comment_id")

            current_comment = self.comment_model.objects.get(id=comment_id)
            current_user = request.user            

            if current_user in current_comment.like.all():
                current_comment.like.remove(current_user)
            else:
                current_comment.like.add(current_user)

            return render(request, "partials/comment_like_count.html" , {'comment':current_comment})
        