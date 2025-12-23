"""
URL Configuration for CropPulse Africa project
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API endpoints
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/weather/', include('apps.weather.urls')),
    path('api/v1/observations/', include('apps.observations.urls')),
    path('api/v1/alerts/', include('apps.alerts.urls')),
    path('api/v1/community/', include('apps.community.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site configuration
admin.site.site_header = 'CropPulse Africa Administration'
admin.site.site_title = 'CropPulse Africa Admin'
admin.site.index_title = 'Welcome to CropPulse Africa Administration'
