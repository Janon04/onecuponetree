from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta

class OneCupAdminSite(AdminSite):
    site_title = "One Cup Initiative Admin"
    site_header = "One Cup Initiative Administration"
    index_title = "Dashboard"
    
    def index(self, request, extra_context=None):
        """
        Custom admin index view with statistics
        """
        extra_context = extra_context or {}
        
        # Import models here to avoid circular imports
        try:
            from farmers.models import Farmer
            from core.models import Donation
            from events.models import Event
            from blog.models import BlogPost
            from accounts.models import User
            
            # Calculate statistics
            now = timezone.now()
            
            stats = {
                'farmers_count': Farmer.objects.count(),
                'total_donations': Donation.objects.filter(
                    payment_status='completed'
                ).aggregate(total=Sum('amount'))['total'] or 0,
                'upcoming_events': Event.objects.filter(
                    start_date__gt=now
                ).count(),
                'blog_posts': BlogPost.objects.filter(
                    is_published=True
                ).count(),
                'total_users': User.objects.count(),
                'recent_farmers': Farmer.objects.filter(
                    interview_date__gte=now - timedelta(days=30)
                ).count(),
                'active_sponsorships': Farmer.objects.filter(
                    sponsorship_is_active=True
                ).count(),
                'pending_donations': Donation.objects.filter(
                    payment_status='pending'
                ).count(),
            }
            
            extra_context['stats'] = stats
            
        except Exception as e:
            # Handle case where models might not be available yet
            extra_context['stats'] = {
                'farmers_count': 0,
                'total_donations': 0,
                'upcoming_events': 0,
                'blog_posts': 0,
            }
        
        return super().index(request, extra_context)

# Create custom admin site instance
admin_site = OneCupAdminSite(name='onecup_admin')