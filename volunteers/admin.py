from django.contrib import admin
from .models import VolunteerOpportunity, VolunteerApplication, BaristaTraining, BaristaTrainingApplication
from django.utils.html import format_html

@admin.register(VolunteerOpportunity)
class VolunteerOpportunityAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_date', 'location', 'is_active', 'media_preview')
	search_fields = ('title', 'description', 'location')
	list_filter = ('is_active', 'start_date')
	readonly_fields = ('media_preview',)

	def media_preview(self, obj):
		if obj.video:
			return format_html('<video width="120" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
		elif obj.image:
			return format_html('<img src="{}" width="120" style="object-fit:cover;" />', obj.image.url)
		return ""
	media_preview.short_description = 'Media Preview'

admin.site.register(VolunteerApplication)
from django.utils.html import format_html

@admin.register(BaristaTraining)
class BaristaTrainingAdmin(admin.ModelAdmin):
	list_display = ('title', 'date', 'location', 'is_active', 'media_preview')
	search_fields = ('title', 'description', 'location')
	list_filter = ('is_active', 'date')
	readonly_fields = ('media_preview',)

	def media_preview(self, obj):
		if obj.video:
			return format_html('<video width="120" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
		elif obj.image:
			return format_html('<img src="{}" width="120" style="object-fit:cover;" />', obj.image.url)
		elif obj.banner:
			return format_html('<img src="{}" width="120" style="object-fit:cover;" />', obj.banner.url)
		return ""
	media_preview.short_description = 'Media Preview'
admin.site.register(BaristaTrainingApplication)