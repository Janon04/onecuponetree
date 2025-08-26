from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_date', 'end_date', 'location', 'status', 'organizer')
	list_filter = ('status', 'start_date', 'location')
	search_fields = ('title', 'description', 'location', 'organizer__username')
	date_hierarchy = 'start_date'
	ordering = ('-start_date',)
