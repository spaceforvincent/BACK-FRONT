from django.shortcuts import render
from django.views.generic import DetailView

from blogapp.models import Post

class PostDV(DetailView):
    model = Post
    template_name = 'blogapp/post_detail.html'



    
