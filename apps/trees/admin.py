from django.contrib import admin
from django.utils.html import format_html
from .models import Tree, TreePlantingSubmission
@admin.register(TreePlantingSubmission)
class TreePlantingSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'tree_type', 'quantity', 'country', 'province', 'district',
        'planting_date', 'contribution_type', 'submitted_at'
    )
    list_filter = ('tree_type', 'country', 'province', 'district', 'contribution_type', 'planting_date', 'submitted_at')
    search_fields = ('full_name', 'contact', 'country', 'province', 'district', 'village', 'reason')
    readonly_fields = ('submitted_at',)

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('tree_id', 'species', 'planted_date', 'planted_by', 'farmer', 'co2_offset', 'media_preview')
    list_filter = ('species', 'planted_date', 'farmer')
    search_fields = ('tree_id', 'species', 'farmer__user__first_name', 'farmer__user__last_name')
    readonly_fields = ('co2_offset', 'media_preview')
    fieldsets = (
        (None, {
            'fields': ('tree_id', 'species', 'planted_date', 'location', 'latitude', 'longitude', 'planted_by', 'farmer', 'photo', 'video', 'media_preview', 'co2_offset', 'is_active')
        }),
    )
    def media_preview(self, obj):
        if obj.video:
            return format_html('<video width="180" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
        elif obj.photo:
            return format_html('<img src="{}" width="120" />', obj.photo.url)
        return ""
    media_preview.short_description = 'Preview'