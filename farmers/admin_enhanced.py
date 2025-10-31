from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Sum
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from .models import (
    Farmer, HouseholdMember, HouseholdAsset, FarmerSupportActivity, 
    FarmerStory, Farm, FarmSponsorship
)
import csv
from django.http import HttpResponse

# Inline classes
class HouseholdMemberInline(admin.TabularInline):
    model = HouseholdMember
    extra = 0
    fields = ('name', 'relationship', 'sex', 'age', 'education_level', 'main_occupation')
    classes = ['collapse']

class HouseholdAssetInline(admin.TabularInline):
    model = HouseholdAsset
    extra = 0
    fields = ('asset_type', 'description', 'quantity', 'house_type')
    classes = ['collapse']

class FarmerStoryInline(admin.StackedInline):
    model = FarmerStory
    extra = 0
    fields = ('title', 'content', 'image', 'is_published')
    classes = ['collapse']

class FarmerSupportActivityInline(admin.TabularInline):
    model = FarmerSupportActivity
    extra = 0
    fields = ('title', 'activity_type', 'date', 'outcome', 'is_public')
    classes = ['collapse']

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'household_id', 'location_info', 'phone_number', 
        'sponsorship_status', 'cooperation_status', 'pinned_status', 'created_date'
    )
    list_filter = (
        'pinned', 'sponsorship_is_active', 'is_coop_member', 'sex', 
        'district', 'main_income_source', 'interview_date'
    )
    search_fields = (
        'full_name', 'household_id', 'phone_number', 'district', 
        'sector', 'cell', 'village', 'interviewer_name'
    )
    readonly_fields = (
        'sponsorship_progress_bar', 'household_summary', 'support_activities_count'
    )
    list_editable = ('pinned',)
    date_hierarchy = 'interview_date'
    ordering = ['-pinned', '-interview_date']
    
    inlines = [HouseholdMemberInline, HouseholdAssetInline, FarmerStoryInline, FarmerSupportActivityInline]
    
    fieldsets = (
        ('Sponsorship Information', {
            'fields': (
                'pinned', 'sponsorship_is_active', 'sponsorship_goal', 
                'sponsorship_received', 'sponsorship_progress_bar', 'sponsorship_description'
            ),
            'classes': ('wide',)
        }),
        ('Basic Information', {
            'fields': (
                'full_name', 'household_id', 'sex', 'age', 'marital_status', 
                'education_level', 'phone_number'
            )
        }),
        ('Location Details', {
            'fields': ('district', 'sector', 'cell', 'village'),
            'classes': ('collapse',)
        }),
        ('Economic Information', {
            'fields': (
                'main_income_source', 'land_size', 'is_coop_member', 
                'coop_name', 'coop_role', 'years_in_coop'
            ),
            'classes': ('collapse',)
        }),
        ('Coffee Farming', {
            'fields': (
                'coffee_trees', 'coffee_production_kg', 'coffee_price_per_kg', 
                'coffee_variety', 'coffee_age_years'
            ),
            'classes': ('collapse',)
        }),
        ('Interview Details', {
            'fields': ('interview_date', 'interviewer_name', 'household_summary'),
            'classes': ('collapse',)
        }),
    )
    
    def location_info(self, obj):
        return f"{obj.district} > {obj.sector} > {obj.cell}"
    location_info.short_description = "Location"
    
    def sponsorship_status(self, obj):
        if obj.sponsorship_is_active:
            progress = obj.sponsorship_progress()
            color = '#28a745' if progress >= 100 else '#ffc107' if progress >= 50 else '#dc3545'
            return format_html(
                '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">'
                'Active ({}%)</span>',
                color, progress
            )
        return format_html(
            '<span style="background: #6c757d; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">'
            'Inactive</span>'
        )
    sponsorship_status.short_description = "Sponsorship"
    
    def cooperation_status(self, obj):
        if obj.is_coop_member:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">'
                'Member</span>'
            )
        return format_html(
            '<span style="background: #6c757d; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">'
            'Not Member</span>'
        )
    cooperation_status.short_description = "Cooperative"
    
    def pinned_status(self, obj):
        if obj.pinned:
            return format_html('<i class="fas fa-thumbtack" style="color: #d4af37;"></i>')
        return ""
    pinned_status.short_description = "📌"
    
    def created_date(self, obj):
        return obj.interview_date.strftime("%b %d, %Y")
    created_date.short_description = "Interview Date"
    created_date.admin_order_field = 'interview_date'
    
    def sponsorship_progress_bar(self, obj):
        if obj.sponsorship_goal and obj.sponsorship_goal > 0:
            progress = obj.sponsorship_progress()
            return format_html(
                '<div style="background: #e9ecef; border-radius: 10px; overflow: hidden; height: 20px; width: 200px;">'
                '<div style="background: #28a745; height: 100%; width: {}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; font-weight: bold;">'
                '{}%</div></div>'
                '<div style="margin-top: 5px; font-size: 12px; color: #666;">'
                '${:,.2f} of ${:,.2f}</div>',
                progress, progress, obj.sponsorship_received, obj.sponsorship_goal
            )
        return "No goal set"
    sponsorship_progress_bar.short_description = "Sponsorship Progress"
    
    def household_summary(self, obj):
        members_count = obj.household_members.count()
        assets_count = obj.household_assets.count()
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">'
            '<strong>Household Overview:</strong><br>'
            'Members: {} people<br>'
            'Assets: {} items<br>'
            'Coffee Trees: {}<br>'
            'Land Size: {} hectares'
            '</div>',
            members_count, assets_count, obj.coffee_trees or 0, obj.land_size or 0
        )
    household_summary.short_description = "Household Summary"
    
    def support_activities_count(self, obj):
        count = obj.support_activities.count()
        recent_count = obj.support_activities.filter(
            date__gte='2024-01-01'  # Adjust date as needed
        ).count()
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">'
            'Total Activities: {}<br>'
            'Recent Activities: {}'
            '</div>',
            count, recent_count
        )
    support_activities_count.short_description = "Support Activities"
    
    actions = ['export_as_csv', 'activate_sponsorship', 'deactivate_sponsorship', 'pin_farmers']
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=farmers_{queryset.count()}_items.csv'
        writer = csv.writer(response)
        
        # Custom header for better export
        headers = [
            'Full Name', 'Household ID', 'Phone', 'District', 'Sector', 'Cell', 'Village',
            'Age', 'Sex', 'Marital Status', 'Education', 'Main Income Source',
            'Coffee Trees', 'Coffee Production (kg)', 'Land Size', 'Coop Member',
            'Sponsorship Active', 'Sponsorship Goal', 'Sponsorship Received',
            'Interview Date', 'Interviewer'
        ]
        writer.writerow(headers)
        
        for obj in queryset:
            writer.writerow([
                obj.full_name, obj.household_id, obj.phone_number,
                obj.district, obj.sector, obj.cell, obj.village,
                obj.age, obj.get_sex_display(), obj.get_marital_status_display(),
                obj.get_education_level_display(), obj.main_income_source,
                obj.coffee_trees, obj.coffee_production_kg, obj.land_size,
                'Yes' if obj.is_coop_member else 'No',
                'Yes' if obj.sponsorship_is_active else 'No',
                obj.sponsorship_goal, obj.sponsorship_received,
                obj.interview_date, obj.interviewer_name
            ])
        return response
    export_as_csv.short_description = "Export selected farmers as CSV"
    
    def activate_sponsorship(self, request, queryset):
        updated = queryset.update(sponsorship_is_active=True)
        self.message_user(request, f'{updated} farmers activated for sponsorship.')
    activate_sponsorship.short_description = "Activate sponsorship for selected farmers"
    
    def deactivate_sponsorship(self, request, queryset):
        updated = queryset.update(sponsorship_is_active=False)
        self.message_user(request, f'{updated} farmers deactivated from sponsorship.')
    deactivate_sponsorship.short_description = "Deactivate sponsorship for selected farmers"
    
    def pin_farmers(self, request, queryset):
        updated = queryset.update(pinned=True)
        self.message_user(request, f'{updated} farmers pinned to top.')
    pin_farmers.short_description = "Pin selected farmers to top"

@admin.register(HouseholdMember)
class HouseholdMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'relationship', 'sex', 'age', 'education_level', 'main_occupation')
    list_filter = ('relationship', 'sex', 'education_level', 'school_attendance')
    search_fields = ('name', 'farmer__full_name', 'main_occupation')
    ordering = ['farmer__full_name', 'age']

@admin.register(HouseholdAsset)
class HouseholdAssetAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'asset_type', 'description', 'quantity', 'house_type')
    list_filter = ('asset_type', 'house_type')
    search_fields = ('farmer__full_name', 'description')
    ordering = ['farmer__full_name']

@admin.register(FarmerSupportActivity)
class FarmerSupportActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'date', 'location', 'staff_name', 'farmers_count', 'public_status')
    list_filter = ('activity_type', 'date', 'is_public', 'staff')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('farmers_count_display',)
    date_hierarchy = 'date'
    ordering = ['-date']
    
    filter_horizontal = ('farmers',)
    
    def staff_name(self, obj):
        return obj.staff.get_full_name() if obj.staff else "Not assigned"
    staff_name.short_description = "Staff Member"
    
    def farmers_count(self, obj):
        return obj.farmers.count()
    farmers_count.short_description = "Farmers"
    
    def public_status(self, obj):
        if obj.is_public:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">Public</span>'
            )
        return format_html(
            '<span style="background: #6c757d; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">Private</span>'
        )
    public_status.short_description = "Visibility"
    
    def farmers_count_display(self, obj):
        count = obj.farmers.count()
        farmers_list = obj.farmers.all()[:5]  # Show first 5
        
        html = f'<div><strong>Total: {count} farmers</strong></div>'
        if farmers_list:
            html += '<div style="margin-top: 8px;">'
            for farmer in farmers_list:
                html += f'<div style="margin: 2px 0;">• {farmer.full_name}</div>'
            if count > 5:
                html += f'<div style="color: #666; font-style: italic;">... and {count - 5} more</div>'
            html += '</div>'
        
        return format_html(html)
    farmers_count_display.short_description = "Participating Farmers"

@admin.register(FarmerStory)
class FarmerStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'farmer', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content', 'farmer__full_name')
    readonly_fields = ('image_preview',)
    ordering = ['-created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'sponsorship_status', 'sponsorship_progress', 'created_at')
    list_filter = ('sponsorship_is_active', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'location')
    readonly_fields = ('image_preview', 'sponsorship_stats')
    ordering = ['-created_at']
    
    def sponsorship_status(self, obj):
        if obj.sponsorship_is_active:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">Active</span>'
            )
        return format_html(
            '<span style="background: #6c757d; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">Inactive</span>'
        )
    sponsorship_status.short_description = "Sponsorship"
    
    def sponsorship_progress(self, obj):
        total = obj.total_sponsorship_amount()
        count = obj.sponsorship_count()
        return f"${total:,.2f} ({count} sponsors)"
    sponsorship_progress.short_description = "Total Sponsored"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"
    
    def sponsorship_stats(self, obj):
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">'
            '<strong>Sponsorship Statistics:</strong><br>'
            'Total Amount: ${:,.2f}<br>'
            'Number of Sponsors: {}<br>'
            'Status: {}'
            '</div>',
            obj.total_sponsorship_amount(),
            obj.sponsorship_count(),
            'Active' if obj.sponsorship_is_active else 'Inactive'
        )
    sponsorship_stats.short_description = "Sponsorship Overview"

@admin.register(FarmSponsorship)
class FarmSponsorshipAdmin(admin.ModelAdmin):
    list_display = ('sponsor_name', 'farm', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sponsor_name', 'sponsor_email', 'farm__name')
    ordering = ['-created_at']