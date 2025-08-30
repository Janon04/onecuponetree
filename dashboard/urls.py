from django.urls import path
from . import views
from .public_views import public_dashboard

urlpatterns = [
    path('', views.impact_dashboard, name='impact'),
    path('public/', public_dashboard, name='public_impact'),
]