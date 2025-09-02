from django.urls import path
from . import views

app_name = 'core'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('donate/', views.donate, name='donate'),
    path('donations/', views.donation_list, name='donation_list'),
    path('subscribe/', views.unified_subscribe, name='unified_subscribe'),
]

