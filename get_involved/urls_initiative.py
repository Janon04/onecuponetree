from django.urls import path
from . import views_initiative as views
from .views_initiative import join_initiative

app_name = 'get_involved'

urlpatterns = [
    path('', views.get_involved, name='get_involved'),
    path('join/', join_initiative, name='join'),
    path('partners/', views.partners, name='partners'),
    # path('donate/', views.donate, name='donate'),  # Removed: use core donation system
    path('thank-you/', views.thank_you, name='thank_you'),
]
