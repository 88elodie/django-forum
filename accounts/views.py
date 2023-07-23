from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Profile, Alert
from posts.models import Post
from django.contrib import messages
from django_drf_filepond.api import store_upload, delete_stored_upload
from django_drf_filepond.models import TemporaryUpload, StoredUpload

# Create your views here.

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def profile(request, user):
    user_info = get_object_or_404(CustomUser, username=user)
    user_posts = Post.objects.filter(author_id=user_info.id).count()
    user_info.num_posts = user_posts
    profile_info = get_object_or_404(Profile, user_id=user_info.id)
    return render(request, 'profile.html', context={"user":user_info, "profile": profile_info})

def EditAccount(request, user):
    user_info = get_object_or_404(CustomUser, username=user)

    if user_info.id != request.user.id:
        messages.info(request, 'you are not allowed to edit this account\'s information')
        return redirect('home')
    
    if request.method == 'GET':
        context = {'form': CustomUserChangeForm(instance=user_info), 'id': user_info.id}
        return render(request, 'registration/edit_account.html', context)
    elif request.method == 'POST':
        account_form = CustomUserChangeForm(request.POST, instance=user_info)
        if account_form.is_valid():
            account_form.save()
            messages.success(request, 'your account information was successfully updated !')
            url = reverse('profile', args=[account_form.instance.username])
            return redirect(url)
        else:
            messages.error(request, 'please correct the following errors')
    return render(request, "registration/edit_account.html", context={"form": account_form})

def EditProfile(request, user):
    user_info = get_object_or_404(CustomUser, username=user)
    profile_info = get_object_or_404(Profile, user_id=user_info.id)

    if user_info.id != request.user.id:
        messages.info(request, 'you are not allowed to edit this account\'s information')
        return redirect('home')
    
    if request.method == 'GET':
        context = {'form': ProfileForm(instance=profile_info), 'id': user_info.id, 'profile': profile_info}
        return render(request, 'profile_form.html', context)
    elif request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile_info)
        if profile_form.is_valid():
            for image in request.POST.getlist('filepond'):
                if image:
                    #get upload name
                    tu = TemporaryUpload.objects.get(upload_id=image)

                    # upload to permanent storage
                    file_info = store_upload(image, str(request.user.id)+'/profile/'+tu.upload_name)
                    profile_form.instance.profile_picture = file_info.file
            profile_form.instance.user_id = user_info.id
            profile_form.save()
            messages.success(request, 'your profile information was successfully updated !')
            url = reverse('profile', args=[user])
            return redirect(url)
        else:
            messages.error(request, 'please correct the following errors')
        return render(request, "profile_form.html", context={"form": profile_form, 'profile': profile_info})
    
def DeletePfp(request, id):
    profile_info = get_object_or_404(Profile, user_id=id)
    su = StoredUpload.objects.get(file=profile_info.profile_picture)
    user_info = CustomUser.objects.get(id=id)

    if id != request.user.id:
        messages.info(request, 'you are not allowed to edit this account\'s information')
        return redirect('home')

    delete_stored_upload(su.upload_id, True)
    profile_info.profile_picture = ""
    profile_info.save()

    messages.success(request, 'your profile picture has been deleted, you can now upload another one')

    url = reverse('edit-profile', args=[user_info.username])
    return redirect(url)

def Alerts(request):
    alerts = Alert.objects.filter(user_id=request.user.id).order_by('-created_at')

    return render(request, "alerts.html", context={"alerts": alerts})
    