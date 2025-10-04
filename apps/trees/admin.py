from django.contrib import admin
from django.utils.html import format_html
from .models import Tree, TreePlantingSubmission
@admin.register(TreePlantingSubmission)
class TreePlantingSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'tree_type', 'quantity', 'country', 'province', 'district',
        'planting_date', 'contribution_type'
    )
    list_filter = ('tree_type', 'country', 'province', 'district', 'contribution_type', 'planting_date')
    search_fields = ('full_name', 'contact', 'country', 'province', 'district', 'village', 'reason')
    # readonly_fields removed: no submitted_at field

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('tree_id', 'species', 'planted_date', 'planted_by', 'farmer', 'co2_offset', 'pinned', 'media_preview')
    list_filter = ('species', 'planted_date', 'farmer')
    search_fields = ('tree_id', 'species', 'farmer__user__first_name', 'farmer__user__last_name')
    readonly_fields = ('co2_offset', 'media_preview')
    fieldsets = (
        (None, {
            'fields': ('tree_id', 'species', 'planted_date', 'location', 'latitude', 'longitude', 'planted_by', 'farmer', 'photo', 'video', 'pinned', 'media_preview', 'co2_offset', 'is_active')
        }),
    )
    def media_preview(self, obj):
        if obj.video:
            return format_html(
                '<a href="#" onclick="var vid=this.nextElementSibling; vid.style.display=\'block\'; this.style.display=\'none\'; return false;">Show Video</a>'
                '<video width="180" controls style="display:none; margin-top:8px;"><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>',
                obj.video.url
            )
        elif obj.photo:
            return format_html(
                '<a href="#" onclick="var img=this.nextElementSibling; img.style.display=\'block\'; this.style.display=\'none\'; return false;">Show Photo</a>'
                '<img src="{}" width="120" style="display:none; margin-top:8px;" />',
                obj.photo.url
            )
        return ""
    media_preview.short_description = 'Preview'