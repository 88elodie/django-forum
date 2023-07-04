from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.http import HttpResponse
from .forms import PostForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Post
import sys

# Create your views here.

def index(request):
    posts = Post.objects.all().prefetch_related("author").order_by('-created_at')
    return render(request, 'posts_index.html', context={"posts": posts})

def SinglePost(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'single_post.html',context={'post': post})

@login_required
def CreatePost(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            print(request.POST)
            # add user to the instance ↓
            post_form.instance.author_id = request.user.id
            post_form.save()
            messages.success(request, 'your post was successfully created!')
            # return redirect('seed:view_seed')
            return redirect('posts')
        else:
            messages.error(request, 'please correct the error below.')
    else:
        post_form = PostForm()
    return render(request, "post_form.html", context={"form": post_form})

def EditPost(request, pk):
    post = get_object_or_404(Post, id=pk)

    if post.author_id != request.user.id:
        messages.info(request, 'you are not allowed to edit this post')
        return redirect('posts')

    if request.method == 'GET':
        context = {'form': PostForm(instance=post), 'id': pk}
        return render(request, 'post_form.html', context)
    elif request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'your post has been updated successfully.')
            post_id = post.id
            url = reverse('single-post', args=[post_id])
            return redirect(url)
        else:
            messages.error(request, 'please correct the following errors')
    return render(request, "post_form.html", context={"form": post_form})

def DeletePost(request, pk):
    post = get_object_or_404(Post, id=pk)

    if post.author_id != request.user.id:
        messages.info(request, 'you are not allowed to delete this post')
        return redirect('posts')
    else:
        post.delete()
        messages.success(request, 'your post has been deleted successfully.')
        return redirect('posts')


