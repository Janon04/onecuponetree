from django.contrib import admin
from django.utils.html import format_html
from .models import ImpactStat, Testimonial

@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
	pass

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = ('author', 'role', 'is_featured', 'created_at', 'media_preview')
	search_fields = ('author', 'role', 'content')
	list_filter = ('is_featured', 'created_at')
	readonly_fields = ('media_preview',)
	fieldsets = (
		(None, {
			'fields': ('author', 'role', 'content', 'photo', 'video', 'media_preview', 'is_featured')
		}),
	)
	def media_preview(self, obj):
		if obj.video:
			return format_html('<video width="180" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
		elif obj.photo:
			return format_html('<img src="{}" width="120" />', obj.photo.url)
		return ""
	media_preview.short_description = 'Preview'