from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('healthz/', lambda r: HttpResponse('ok')),
    path('admin/', admin.site.urls),
    path('', include('src.core.urls', namespace='core')),
    path('leads/', include('src.leads.urls', namespace='leads')),
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
