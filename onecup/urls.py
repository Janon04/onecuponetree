from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('blog/', include('apps.blog.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('farmers/', include('apps.farmers.urls')),
    path('get-involved/', include('apps.get_involved.urls')),
    path('programs/', include('apps.programs.urls')),
    path('shop/', include('apps.shop.urls')),
    path('trees/', include('apps.trees.urls')),
    path('volunteers/', include('apps.volunteers.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)