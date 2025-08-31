from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, BlogCategory

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'created_at', 'is_published', 'media_preview')
	search_fields = ('title', 'description', 'content')
	list_filter = ('is_published', 'created_at', 'author')
	readonly_fields = ('media_preview',)
	fieldsets = (
		(None, {
			'fields': ('title', 'slug', 'author', 'category', 'description', 'content', 'featured_image', 'video', 'media_preview', 'is_published')
		}),
	)
	def media_preview(self, obj):
		if obj.video:
			return format_html('<video width="180" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
		elif obj.featured_image:
			return format_html('<img src="{}" width="120" />', obj.featured_image.url)
		return ""
	media_preview.short_description = 'Preview'

admin.site.register(BlogCategory)