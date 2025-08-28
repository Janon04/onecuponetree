from django.contrib import admin
from .models import Tree

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('tree_id', 'species', 'planted_date', 'planted_by', 'farmer', 'co2_offset')
    list_filter = ('species', 'planted_date', 'farmer')
    search_fields = ('tree_id', 'species', 'farmer__user__first_name', 'farmer__user__last_name')
    readonly_fields = ('co2_offset',)