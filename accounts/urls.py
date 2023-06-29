from django.urls import path
from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('profile/<str:user>/', views.profile, name='profile'),
    path('edit/<str:user>/', views.EditAccount, name='edit-account'),
]
