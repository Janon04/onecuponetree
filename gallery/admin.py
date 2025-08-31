from django.contrib import admin

from django.utils.html import format_html
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'media_preview')
    search_fields = ('title', 'description')
    list_filter = ('uploaded_at',)

    readonly_fields = ('media_preview',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'video', 'media_preview')
        }),
    )

    def media_preview(self, obj):
        if obj.video:
            return format_html('<video width="180" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
        elif obj.image:
            return format_html('<img src="{}" width="120" />', obj.image.url)
        return ""
    media_preview.short_description = 'Preview'
