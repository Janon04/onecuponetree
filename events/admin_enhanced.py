from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count, Q
from .models import Event
import csv
from django.http import HttpResponse

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'status_badge', 'date_range', 'location', 
        'organizer_name', 'attendees_count', 'duration'
    )
    list_filter = ('status', 'start_date', 'organizer')
    search_fields = ('title', 'description', 'location', 'organizer__username')
    readonly_fields = ('event_stats', 'time_until_event')
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'status')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'time_until_event'),
            'classes': ('wide',)
        }),
        ('Details', {
            'fields': ('location', 'organizer'),
        }),
        ('Statistics', {
            'fields': ('event_stats',),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'upcoming': '#17a2b8',
            'ongoing': '#28a745',
            'completed': '#6c757d',
            'cancelled': '#dc3545'
        }
        icons = {
            'upcoming': 'fas fa-clock',
            'ongoing': 'fas fa-play',
            'completed': 'fas fa-check',
            'cancelled': 'fas fa-times'
        }
        
        color = colors.get(obj.status, '#6c757d')
        icon = icons.get(obj.status, 'fas fa-calendar')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">'
            '<i class="{}"></i> {}</span>',
            color, icon, obj.get_status_display()
        )
    status_badge.short_description = "Status"
    status_badge.admin_order_field = 'status'
    
    def date_range(self, obj):
        start = obj.start_date.strftime("%b %d, %Y %H:%M")
        end = obj.end_date.strftime("%b %d, %Y %H:%M")
        
        if obj.start_date.date() == obj.end_date.date():
            # Same day event
            return format_html(
                '<div style="font-size: 13px;">'
                '<strong>{}</strong><br>'
                '<span style="color: #666;">{} - {}</span>'
                '</div>',
                obj.start_date.strftime("%b %d, %Y"),
                obj.start_date.strftime("%H:%M"),
                obj.end_date.strftime("%H:%M")
            )
        else:
            # Multi-day event
            return format_html(
                '<div style="font-size: 13px;">'
                '<strong>From:</strong> {}<br>'
                '<strong>To:</strong> {}'
                '</div>',
                start, end
            )
    date_range.short_description = "Event Schedule"
    date_range.admin_order_field = 'start_date'
    
    def organizer_name(self, obj):
        if obj.organizer:
            full_name = obj.organizer.get_full_name()
            return full_name if full_name else obj.organizer.username
        return "No organizer assigned"
    organizer_name.short_description = "Organizer"
    organizer_name.admin_order_field = 'organizer__username'
    
    def attendees_count(self, obj):
        # This would need to be implemented based on your attendance tracking
        # For now, showing placeholder
        return format_html(
            '<span style="color: #666; font-size: 12px;"><i class="fas fa-users"></i> TBD</span>'
        )
    attendees_count.short_description = "Attendees"
    
    def duration(self, obj):
        duration = obj.end_date - obj.start_date
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    duration.short_description = "Duration"
    
    def time_until_event(self, obj):
        now = timezone.now()
        
        if obj.start_date > now:
            # Future event
            time_diff = obj.start_date - now
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            
            if days > 0:
                return format_html(
                    '<div style="color: #17a2b8; font-weight: 500;">'
                    '<i class="fas fa-clock"></i> Starts in {} days, {} hours'
                    '</div>',
                    days, hours
                )
            elif hours > 0:
                return format_html(
                    '<div style="color: #ffc107; font-weight: 500;">'
                    '<i class="fas fa-clock"></i> Starts in {} hours'
                    '</div>',
                    hours
                )
            else:
                return format_html(
                    '<div style="color: #dc3545; font-weight: 500;">'
                    '<i class="fas fa-clock"></i> Starting soon!'
                    '</div>'
                )
        elif obj.start_date <= now <= obj.end_date:
            # Ongoing event
            time_diff = obj.end_date - now
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            return format_html(
                '<div style="color: #28a745; font-weight: 500;">'
                '<i class="fas fa-play"></i> Ongoing ({}h {}m remaining)'
                '</div>',
                hours, minutes
            )
        else:
            # Past event
            time_diff = now - obj.end_date
            days = time_diff.days
            
            return format_html(
                '<div style="color: #6c757d; font-weight: 500;">'
                '<i class="fas fa-check"></i> Ended {} days ago'
                '</div>',
                days
            )
    time_until_event.short_description = "Timing"
    
    def event_stats(self, obj):
        now = timezone.now()
        
        # Get some context stats
        total_events = Event.objects.count()
        upcoming_events = Event.objects.filter(start_date__gt=now).count()
        ongoing_events = Event.objects.filter(start_date__lte=now, end_date__gte=now).count()
        
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">'
            '<strong>Platform Statistics:</strong><br>'
            'Total Events: {}<br>'
            'Upcoming: {}<br>'
            'Ongoing: {}<br>'
            '<hr style="margin: 8px 0;">'
            '<strong>This Event:</strong><br>'
            'Duration: {}<br>'
            'Status: {}'
            '</div>',
            total_events, upcoming_events, ongoing_events,
            self.duration(obj), obj.get_status_display()
        )
    event_stats.short_description = "Event Statistics"
    
    actions = ['mark_as_completed', 'mark_as_cancelled', 'export_as_csv']
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} events marked as completed.')
    mark_as_completed.short_description = "Mark selected events as completed"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} events marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected events as cancelled"
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=events_{queryset.count()}_items.csv'
        writer = csv.writer(response)
        
        headers = [
            'Title', 'Status', 'Start Date', 'End Date', 'Location',
            'Organizer', 'Duration (minutes)', 'Description'
        ]
        writer.writerow(headers)
        
        for obj in queryset:
            duration_minutes = int((obj.end_date - obj.start_date).total_seconds() / 60)
            writer.writerow([
                obj.title,
                obj.get_status_display(),
                obj.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                obj.end_date.strftime('%Y-%m-%d %H:%M:%S'),
                obj.location,
                obj.organizer.get_full_name() if obj.organizer else '',
                duration_minutes,
                obj.description
            ])
        return response
    export_as_csv.short_description = "Export selected events as CSV"
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }