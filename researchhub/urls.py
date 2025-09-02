from django.urls import path
from . import views

app_name = 'researchhub'

urlpatterns = [
    path('', views.publication_list, name='publication_list'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('categories/manage/', views.category_manage, name='category_manage'),
    path('download-requests/', views.publication_download_requests, name='publication_download_requests'),
    path('<int:pk>/download/', views.publication_secure_download, name='publication_secure_download'),
    path('<int:pk>/', views.publication_detail, name='publication_detail'),
]
