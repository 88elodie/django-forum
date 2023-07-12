from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Profile
from posts.models import Post
from django.contrib import messages

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
    return render(request, 'profile.html', context={"user":user_info})

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
            messages.success(request, 'your account information has been updated successfully.')
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
        context = {'id': user_info.id}
        return render(request, 'profile_form.html', context)
