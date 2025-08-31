from django.contrib import admin
from .models import Event

from django.utils.html import format_html

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_date', 'end_date', 'location', 'status', 'organizer', 'media_preview')
	list_filter = ('status', 'start_date', 'location')
	search_fields = ('title', 'description', 'location', 'organizer__username')
	date_hierarchy = 'start_date'
	ordering = ('-start_date',)
	readonly_fields = ('media_preview',)
	fieldsets = (
		(None, {
			'fields': ('title', 'description', 'start_date', 'end_date', 'location', 'organizer', 'status', 'image', 'video', 'media_preview')
		}),
	)
	def media_preview(self, obj):
		if obj.video:
			return format_html('<video width="180" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
		elif obj.image:
			return format_html('<img src="{}" width="120" />', obj.image.url)
		return ""
	media_preview.short_description = 'Preview'
