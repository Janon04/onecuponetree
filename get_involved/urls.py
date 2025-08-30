from django.urls import path
from . import views

app_name = 'get_involved'

urlpatterns = [
    path('', views.get_involved, name='get_involved'),
    path('join/', views.join_initiative, name='join'),
    path('partners/', views.partners, name='partners'),
    path('volunteers/', views.volunteers, name='volunteers'),
    # path('donate/', views.donate, name='donate'),  # Removed: use core donation system
    path('thank-you/', views.thank_you, name='thank_you'),
]