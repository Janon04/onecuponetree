from django.urls import path
from . import views

app_name = 'volunteers'
urlpatterns = [
    path('opportunities/', views.volunteer_opportunities, name='opportunities'),
    path('opportunities/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('apply/<int:pk>/', views.apply_opportunity, name='apply'),
    path('barista-training/', views.barista_training, name='barista_training'),
]