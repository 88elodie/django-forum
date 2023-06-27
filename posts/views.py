from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import PostForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Post

# Create your views here.

def index(request):
    posts = Post.objects.all().prefetch_related("author").order_by('-created_at')
    return render(request, 'posts_index.html', context={"posts": posts})

def SinglePost(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'single_post.html',context={'post': post})

@login_required
def CreatePost(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            # add user to the instance ↓
            post_form.instance.user = request.user
            post_form.save()
            messages.success(request, 'Your post was successfully created!')
            # return redirect('seed:view_seed')
            return redirect('posts')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        post_form = PostForm()
    return render(request, "create_post.html", context={"form": post_form})
