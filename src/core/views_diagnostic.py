"""Діагностика деплою — що бачить запущений процес Passenger."""

from __future__ import annotations

import inspect
import subprocess
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse, HttpRequest


def deploy_health(request: HttpRequest):
    from src.core.templatetags import site_tags
    from src.core.templatetags.site_tags import content_image_url

    sample = 'marking/cij/linx_8900.jpg'
    static_rel = f'content/{sample}'
    static_root = Path(settings.STATIC_ROOT)
    base_dir = Path(settings.BASE_DIR)

    git_head = ''
    try:
        git_head = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            cwd=base_dir,
            text=True,
            timeout=3,
        ).strip()
    except Exception as exc:
        git_head = f'error: {exc}'

    storage = getattr(settings, 'STATICFILES_STORAGE', '')
    storages = getattr(settings, 'STORAGES', {})

    data = {
        'git_head': git_head,
        'django_settings': settings.SETTINGS_MODULE,
        'base_dir': str(base_dir),
        'static_root': str(static_root),
        'media_root': str(settings.MEDIA_ROOT),
        'static_url': settings.STATIC_URL,
        'staticfiles_storage': storage,
        'storages_staticfiles': storages.get('staticfiles', {}),
        'site_tags_file': inspect.getfile(site_tags),
        'content_image_url': content_image_url(sample),
        'checks': {
            'staticfiles_content': (static_root / static_rel).is_file(),
            'static_source_content': (base_dir / 'static' / static_rel).is_file(),
            'media_file': (Path(settings.MEDIA_ROOT) / sample).is_file(),
            'www_dir': (base_dir / 'www').is_dir(),
            'www_staticfiles_content': (base_dir / 'www' / 'staticfiles' / static_rel).is_file(),
            'passenger_wsgi': (base_dir / 'passenger_wsgi.py').is_file(),
            'admin_py_removed': not (base_dir / 'src' / 'content' / 'admin.py').is_file(),
            'admin_package': (base_dir / 'src' / 'content' / 'admin' / '__init__.py').is_file(),
        },
    }
    if (static_root / static_rel).is_file():
        data['checks']['staticfiles_content_size'] = (static_root / static_rel).stat().st_size

    try:
        from django.contrib import admin
        from src.content.models import MarkingPage
        from src.content.admin_sidebar import ADMIN_SIDEBAR

        marking_admin = admin.site._registry.get(MarkingPage)
        if marking_admin:
            cls = marking_admin.__class__
            fieldsets = getattr(cls, 'fieldsets', None) or []
            data['admin_runtime'] = {
                'marking_admin_class': f'{cls.__module__}.{cls.__name__}',
                'marking_fieldsets': [row[0] for row in fieldsets],
                'sidebar_first_section': ADMIN_SIDEBAR['navigation'][0]['title'],
                'admin_links_ok': any('Картки' in title for title, _ in fieldsets),
            }
    except Exception as exc:
        data['admin_runtime'] = {'error': str(exc)}

    return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 2})
