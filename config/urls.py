from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('healthz/', lambda r: HttpResponse('ok')),
    path('admin/', admin.site.urls),
    path('', include('src.core.urls', namespace='core')),
    path('leads/', include('src.leads.urls', namespace='leads')),
]

if settings.DEBUG or getattr(settings, 'SERVE_MEDIA', False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
