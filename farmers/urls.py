from django.urls import path


from . import views

urlpatterns = [
    path('sponsor-a-farm/', views.farm_list, name='farm_list'),
    path('sponsor-a-farm/<int:pk>/', views.farm_detail, name='farm_detail'),
    path('', views.farmer_list, name='list'),
    path('support/', views.farmer_support_list, name='farmer_support_list'),
    path('support-activities/', views.support_activities_public, name='support_activities_public'),
    path('stories/', views.story_list, name='story_list'),
    path('<int:pk>/', views.farmer_detail, name='detail'),
]