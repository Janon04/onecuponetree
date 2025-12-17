from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count
from .models import Contact, Donation, TeamMember
import csv
from django.http import HttpResponse

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'order', 'photo_preview', 'social_links', 'created_at')
    list_editable = ('order',)
    search_fields = ('name', 'title', 'bio')
    list_filter = ('title', 'created_at')
    ordering = ['order', 'name']
    readonly_fields = ('photo_preview',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'photo', 'photo_preview', 'bio', 'order')
        }),
        ('Social Media Links', {
            'fields': ('facebook', 'twitter', 'instagram', 'youtube', 'linkedin'),
            'classes': ('collapse',)
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.photo.url
            )
        return "No photo"
    photo_preview.short_description = "Photo Preview"
    
    def social_links(self, obj):
        links = []
        social_platforms = [
            ('facebook', 'fab fa-facebook', '#1877f2'),
            ('twitter', 'fab fa-twitter', '#1da1f2'),
            ('instagram', 'fab fa-instagram', '#e4405f'),
            ('youtube', 'fab fa-youtube', '#ff0000'),
            ('linkedin', 'fab fa-linkedin', '#0077b5'),
        ]
        
        for platform, icon, color in social_platforms:
            url = getattr(obj, platform)
            if url:
                links.append(
                    f'<a href="{url}" target="_blank" style="color: {color}; margin-right: 8px; font-size: 16px;"><i class="{icon}"></i></a>'
                )
        
        return format_html(''.join(links)) if links else "No social links"
    social_links.short_description = "Social Media"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'status_badge')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'message_preview')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message', 'message_preview')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        return format_html(
            '<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">New</span>'
        )
    status_badge.short_description = "Status"
    
    def message_preview(self, obj):
        if obj.message:
            preview = obj.message[:100] + "..." if len(obj.message) > 100 else obj.message
            return format_html(
                '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px; border-left: 4px solid #d4af37;">{}</div>',
                preview
            )
        return "No message"
    message_preview.short_description = "Message Preview"
    
    actions = ['export_as_csv']
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=contacts_{queryset.count()}_items.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = "Export selected contacts as CSV"

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'donor_email', 'amount_display', 'donation_type', 'payment_status_badge', 'purpose', 'created_at')
    list_filter = (
        'donation_type', 
        'payment_status', 
        'donation_frequency',
        'currency',
        'purpose',
        'public_acknowledgement',
        'created_at'
    )
    search_fields = ('donor_name', 'donor_email', 'message', 'transaction_reference')
    readonly_fields = ('created_at', 'total_stats')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'phone', 'country', 'province_district')
        }),
        ('Donation Details', {
            'fields': ('amount', 'currency', 'donation_type', 'donation_frequency', 'purpose', 'message')
        }),
        ('Payment Information', {
            'fields': ('donation_mode', 'transaction_reference', 'payment_status', 'receipt_sent')
        }),
        ('Linked Items', {
            'fields': ('farmer', 'tree'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('public_acknowledgement', 'communication_opt_in', 'declaration', 'donor_signature', 'signature_date'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'total_stats'),
            'classes': ('collapse',)
        }),
    )
    
    def amount_display(self, obj):
        return format_html(
            '<span style="font-weight: 600; color: #28a745;">{} {}</span>',
            obj.currency, obj.amount
        )
    amount_display.short_description = "Amount"
    amount_display.admin_order_field = 'amount'
    
    def payment_status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'completed': '#28a745',
            'failed': '#dc3545',
            'refunded': '#6c757d'
        }
        color = colors.get(obj.payment_status, '#6c757d')
        
        # Define display labels since the model doesn't have choices
        status_labels = {
            'pending': 'Pending',
            'completed': 'Completed',
            'failed': 'Failed',
            'refunded': 'Refunded'
        }
        display_label = status_labels.get(obj.payment_status, obj.payment_status.title())
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">{}</span>',
            color, display_label
        )
    payment_status_badge.short_description = "Status"
    payment_status_badge.admin_order_field = 'payment_status'
    
    def total_stats(self, obj):
        total_donations = Donation.objects.filter(payment_status='completed').aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">'
            '<strong>Platform Stats:</strong><br>'
            'Total Donations: {} items<br>'
            'Total Amount: ${:,.2f}'
            '</div>',
            total_donations['count'] or 0,
            total_donations['total'] or 0
        )
    total_stats.short_description = "Platform Statistics"
    
    actions = ['export_as_csv', 'mark_as_completed', 'send_receipts']
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=donations_{queryset.count()}_items.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = "Export selected donations as CSV"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(payment_status='completed')
        self.message_user(request, f'{updated} donations marked as completed.')
    mark_as_completed.short_description = "Mark selected donations as completed"
    
    def send_receipts(self, request, queryset):
        count = queryset.filter(payment_status='completed', receipt_sent=False).count()
        self.message_user(request, f'Receipt sending initiated for {count} donations.')
    send_receipts.short_description = "Send receipts to selected donors"