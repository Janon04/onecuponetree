
from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('blog/', views.blog_list.as_view(), name='post_list'),
    path('blog/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
]
