from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'volunteers'
urlpatterns = [
    path('opportunities/', views.volunteer_opportunities, name='opportunities'),
    path('opportunities/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('apply/<int:pk>/', views.apply_opportunity, name='apply'),
    path('barista-training/', RedirectView.as_view(pattern_name='volunteers:barista_training_list', permanent=True)),
    path('barista-trainings/', views.barista_training_list, name='barista_training_list'),
    path('barista-trainings/<int:pk>/', views.barista_training_detail, name='barista_training_detail'),
    path('barista-trainings/<int:pk>/apply/', views.barista_training_apply, name='barista_training_apply'),
]