from django.conf import settings


def site_settings(request):
    """Add site-wide settings to template context"""
    return {
        # Site Information
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'One Cup Initiative'),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION', ''),
        
        # Contact Information
        'CONTACT_EMAIL': getattr(settings, 'CONTACT_EMAIL', ''),
        'CONTACT_PHONE': getattr(settings, 'CONTACT_PHONE', ''),
        'CONTACT_ADDRESS': getattr(settings, 'CONTACT_ADDRESS', ''),
        'CONTACT_MAP_URL': getattr(settings, 'CONTACT_MAP_URL', ''),
        'CONTACT_NOTIFICATION_EMAIL': getattr(settings, 'CONTACT_NOTIFICATION_EMAIL', ''),
        
        # Social Media Links
        'SOCIAL_MEDIA_LINKS': getattr(settings, 'SOCIAL_MEDIA_LINKS', {}),
    }

