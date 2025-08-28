from django.shortcuts import render


from django.views.generic import ListView
from .models import Program

class ProgramListView(ListView):
	model = Program
	template_name = 'programs/program_list.html'
	context_object_name = 'programs'
	queryset = Program.objects.filter(is_active=True)
