""" from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Tree

@admin.register(Tree)
class TreeAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    list_display = ('tree_id', 'species', 'planted_date', 'planted_by', 'farmer', 'co2_offset')
    list_filter = ('species', 'planted_date', 'farmer')
    search_fields = ('tree_id', 'species', 'farmer__user__first_name', 'farmer__user__last_name')
    readonly_fields = ('co2_offset',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(is_active=True)
        return qs """