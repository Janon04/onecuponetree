from django.urls import path
from . import views

urlpatterns = [
    path('', views.farmer_list, name='list'),
    path('support/', views.farmer_support_list, name='farmer_support_list'),
    path('support-activities/', views.support_activities_public, name='support_activities_public'),
    path('<int:pk>/', views.farmer_detail, name='detail'),
]