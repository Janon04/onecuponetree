from django.urls import path

app_name = 'contact'

from .views import contact_view

urlpatterns = [
    path('', contact_view, name='contact'),
]
