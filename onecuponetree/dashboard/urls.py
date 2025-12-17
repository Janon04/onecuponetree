from django.urls import path
from . import views
from .public_views import public_dashboard

urlpatterns = [
    # Backend-only dashboard endpoint (redirects to home, or returns JSON with ?format=json)
    path('', views.impact_dashboard, name='impact'),
    path('public/', public_dashboard, name='public_impact'),
]