from django.contrib import admin
from .models import Program

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
	list_display = ('name', 'is_active', 'created_at')
	search_fields = ('name', 'description')
	list_filter = ('is_active',)
