from django.urls import path

app_name = 'programs'

from .views import ProgramListView

urlpatterns = [
    path('', ProgramListView.as_view(), name='program_list'),
]
