from django.urls import path
from . import views

urlpatterns = [
    path('<str:board>/', views.index, name='posts'),
    path('create/', views.CreatePost, name='create-post'),
    path('<int:pk>/', views.SinglePost, name='single-post'),
    path('edit/<int:pk>/', views.EditPost, name='edit-post'),
    path('delete/<int:pk>/', views.DeletePost, name='delete-post'),
]
