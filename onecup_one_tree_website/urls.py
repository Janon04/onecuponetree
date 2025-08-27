from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Add for language switching
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('programs/', include('programs.urls')),
    path('shop/', include('shop.urls')),
    #path('media/', include('media.urls')),
    path('events/', include('events.urls')),
    path('contact/', include('contact.urls')),
    path('api/', include('api.urls')),
    path('blogs/', include('blog.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
