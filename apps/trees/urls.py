from django.urls import path
from . import views

app_name = 'trees'
urlpatterns = [
    path("", views.TreeListView.as_view(), name="list"),
    path("<int:pk>/", views.TreeDetailView.as_view(), name="detail"),
    path('track/', views.track_tree, name='track'),
    path('plant/', views.plant_tree, name='plant_tree'),
]