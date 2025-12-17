from django.contrib import admin
from .models import ResearchPublication, ResearchCategory, PublicationDownloadRequest
@admin.register(PublicationDownloadRequest)
class PublicationDownloadRequestAdmin(admin.ModelAdmin):
	list_display = ('publication', 'name', 'email', 'approved', 'requested_at', 'approved_at')
	list_filter = ('approved', 'requested_at', 'approved_at')
	search_fields = ('name', 'email', 'reason', 'publication__title')
	ordering = ('-requested_at',)

@admin.register(ResearchCategory)
class ResearchCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'is_active')
	search_fields = ('name',)
	ordering = ('name',)

@admin.register(ResearchPublication)
class ResearchPublicationAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'author', 'publication_date', 'is_active', 'created_at')
	list_filter = ('is_active', 'publication_date', 'category')
	search_fields = ('title', 'author', 'summary')
	ordering = ('-publication_date', '-created_at')
