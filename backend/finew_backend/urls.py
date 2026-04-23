"""
URL configuration for finew_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/budgets/', include('apps.budgets.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
]
