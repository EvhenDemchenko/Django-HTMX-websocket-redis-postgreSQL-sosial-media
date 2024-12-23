from django.shortcuts import render

from django.views.generic import View 
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
# Create your views here.

class HomePage(View):
    def get(self,request , *args , **kwargs):
        if not request.user.is_authenticated: 
            return render (request , 'z_home/home_page.html')
        if request.user.is_authenticated:
            return redirect('posts:post-feed')
  