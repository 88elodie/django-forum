from django.urls import path
from .views import SignUpView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('profile/<str:user>/', views.profile, name='profile'),
    path('profile/edit/<str:user>/', views.EditProfile, name='edit-profile'),
    path('edit/<str:user>/', views.EditAccount, name='edit-account'),
    path('profile/deletepfp/<int:id>/', views.DeletePfp, name='delete-pfp')
]
