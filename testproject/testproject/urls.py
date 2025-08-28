"""
URL configuration for testproject project.
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('random_quote.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
