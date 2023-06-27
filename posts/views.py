from django.shortcuts import render
from django.http import HttpResponse
from .forms import PostForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'posts_index.html')

class CreatePost(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    success_url = reverse_lazy("posts")
    template_name = "create_post.html"
