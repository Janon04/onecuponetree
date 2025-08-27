
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='post_list'),
    path('<slug:slug>/', views.blog_detail, name='post_detail'),
]
