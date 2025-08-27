from django.urls import path
from . import views

urlpatterns = [
    path('', views.farmer_list, name='list'),
    path('<int:pk>/', views.farmer_detail, name='detail'),
]