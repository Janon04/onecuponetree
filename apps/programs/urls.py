from django.urls import path
from . import views

app_name = 'programs'
urlpatterns = [
    path('', views.programs, name='programs'),
    path('barista-academy/', views.barista_academy, name='barista_academy'),
    path('farmer-support/', views.farmer_support, name='farmer_support'),
    path('reusable-cups/', views.reusable_cups, name='reusable_cups'),
]