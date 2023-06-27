from django.urls import path
from . import views
from .views import CreatePost

urlpatterns = [
    path('', views.index, name='posts'),
    path('create/', CreatePost.as_view(), name='create-posts'),
]
