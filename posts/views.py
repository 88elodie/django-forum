from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404, reverse
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, File, Comment, Board
from accounts.models import Profile, Alert
from django_drf_filepond.api import store_upload, delete_stored_upload
from django_drf_filepond.models import TemporaryUpload
from django.core import serializers

# Create your views here.

def index(request, board):
    board = Board.objects.filter(slug=board).first()
    posts = Post.objects.prefetch_related("author").order_by('-created_at').filter(board_id=board.id)

    return render(request, 'posts_index.html', context={"posts": posts, 'board': board})

def SinglePost(request, pk):
    post = Post.objects.filter(id=pk).first()
    files = File.objects.filter(post_id=pk)
    author_profile = get_object_or_404(Profile, user_id=post.author_id)
    comments = Comment.objects.filter(post_id=pk)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_post = CommentForm(request.POST)
        if comment_post.is_valid():
            # add user to the instance ↓
            comment_post.instance.user_id = request.user.id
            comment_post.instance.post_id = pk
            comment = comment_post.save()

            # comment alert to post author
            if post.author_id != request.user.id:
                alert = Alert()
                alert.user_id = post.author_id
                alert.alerter_id = request.user.id
                alert.alert_type = "comment"
                alert.post_id = post.id
                alert.save()

            messages.success(request, 'your comment was posted !')
            url = reverse('single-post', args=[pk])
            return redirect(url)
        
    return render(request, 'single_post.html',context={'post': post, 'images': files, 'author_profile': author_profile, 'form': comment_form, 'comments': comments})




@login_required
def CreatePost(request, board):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            # add user to the instance ↓
            post_form.instance.author_id = request.user.id
            # add board to the instance ↓
            post_form.instance.board_id = board
            post = post_form.save()

            
            # upload files in permanent folder and save to database
            for image in request.POST.getlist('filepond'):
                if image:
                    #get upload name
                    tu = TemporaryUpload.objects.get(upload_id=image)

                    # upload to permanent storage
                    file_info = store_upload(image, str(request.user.id)+'/'+str(post.id)+'/'+tu.upload_name)
                    # create File object and assign data
                    post_file = File()

                    post_file.upload_id = file_info.upload_id
                    post_file.file = file_info.file
                    post_file.post_id = post.id
                    post_file.uploaded_by_id = request.user.id
                    # save file object to DB
                    post_file.save()

            messages.success(request, 'your post was successfully created !')
            # return redirect('seed:view_seed')
            board = Board.objects.filter(id=board).first()
            url = reverse('single-post', args=[post.id])
            return redirect(url)
        else:
            messages.error(request, 'please correct the error below')
    else:
        post_form = PostForm()
    return render(request, "post_form.html", context={"form": post_form})

def EditPost(request, pk):
    post = get_object_or_404(Post, id=pk)
    files = File.objects.filter(post_id=pk)
    filesJson = serializers.serialize('json', files)

    if post.author_id != request.user.id:
        messages.info(request, 'you are not allowed to edit this post')
        return redirect('posts')

    if request.method == 'GET':
        context = {'form': PostForm(instance=post), 'id': pk, 'files': files, 'filesJson': filesJson}
        return render(request, 'post_form.html', context)
    elif request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'your post was successfully updated !')
            post_id = post.id

            # upload files in permanent folder and save to database
            for image in request.POST.getlist('filepond'):
                if image:
                    #get upload name
                    tu = TemporaryUpload.objects.get(upload_id=image)

                    # upload to permanent storage
                    file_info = store_upload(image, str(request.user.id)+'/'+str(post.id)+'/'+tu.upload_name)
                    # create File object and assign data
                    post_file = File()

                    post_file.upload_id = file_info.upload_id
                    post_file.file = file_info.file
                    post_file.post_id = post.id
                    post_file.uploaded_by_id = request.user.id
                    # save file object to DB
                    post_file.save()

            url = reverse('single-post', args=[post_id])
            return redirect(url)
        else:
            messages.error(request, 'please correct the following errors')
    return render(request, "post_form.html", context={"form": post_form, "files": files, 'filesJson': filesJson})

def DeletePost(request, pk):
    post = get_object_or_404(Post, id=pk)
    board = Board.objects.filter(id=post.board_id).first()

    if post.author_id != request.user.id:
        messages.info(request, 'you are not allowed to delete this post')
        url = reverse('posts', args=[board.slug])
        return redirect(url)
    else:
        files = File.objects.filter(post_id=pk)
        for file in files:
            delete_stored_upload(file.upload_id, True)
            file.delete()
        post.delete()
        messages.success(request, 'your post has been deleted successfully.')
        url = reverse('posts', args=[board.slug])
        return redirect(url)
    
def DeleteImg(request, id):
    img_file = get_object_or_404(File, id=id)

    if img_file.uploaded_by_id != request.user.id:
        messages.info(request, 'you are not allowed to perform this action')
        return redirect('home')

    delete_stored_upload(img_file.upload_id, True)
    img_file.delete()

    messages.success(request, 'your image has been deleted, you can now upload another one')

    url = reverse('edit-post', args=[img_file.post_id])
    return redirect(url)


