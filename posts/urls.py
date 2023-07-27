from django.urls import path
from . import views

urlpatterns = [
    path('<str:board>/', views.index, name='posts'),
    path('create/<int:board>/', views.CreatePost, name='create-post'),
    path('post/<int:pk>/', views.SinglePost, name='single-post'),
    path('edit/<int:pk>/', views.EditPost, name='edit-post'),
    path('delete/<int:pk>/', views.DeletePost, name='delete-post'),
    path('deleteimg/<int:id>/', views.DeleteImg, name='delete-img'),
    path('delete-comment/<int:pk>/', views.DeleteComment, name='delete-comment'),
]
