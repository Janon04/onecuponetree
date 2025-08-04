from django.urls import path
from . import views

urlpatterns = [
    path('', views.impact_dashboard, name='impact'),
]