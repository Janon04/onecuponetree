from django.conf import settings


def site_settings(request):
    """Add site-wide settings to template context"""
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'One Cup One Tree Initiative'),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION', ''),
        'CONTACT_EMAIL': getattr(settings, 'CONTACT_EMAIL', ''),
        'SOCIAL_MEDIA_LINKS': getattr(settings, 'SOCIAL_MEDIA_LINKS', {}),
    }

