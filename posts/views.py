from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.http import HttpResponse
from .forms import PostForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Post, File
from django_drf_filepond.api import store_upload, delete_stored_upload

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
            # add user to the instance ↓
            post_form.instance.author_id = request.user.id
            post = post_form.save()

            # upload files in permanent folder and save to database
            id = 1
            for image in request.POST.getlist('filepond'):
                file_info = store_upload(image, str(request.user.id)+'/'+str(post.id)+'/image'+str(id))
                id = id + 1
                post_file = File()

                post_file.upload_id = file_info.upload_id
                post_file.file = file_info.file
                post_file.post_id = post.id
                post_file.uploaded_by_id = request.user.id

                post_file.save()

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
        files = File.objects.filter(post_id=pk)
        for file in files:
            delete_stored_upload(file.upload_id, True)
            file.delete()
        post.delete()
        messages.success(request, 'your post has been deleted successfully.')
        return redirect('posts')


