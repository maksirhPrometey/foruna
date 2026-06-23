"""Синхронізація staticfiles у www/ для ADM.TOOLS nginx."""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from src.core.content_data.io import sync_staticfiles_to_www


class Command(BaseCommand):
    help = 'Копіює staticfiles/ → www/staticfiles/ (ADM.TOOLS nginx docroot)'

    def handle(self, *args, **options):
        base = Path(settings.BASE_DIR)
        static_root = Path(settings.STATIC_ROOT)
        ok, message = sync_staticfiles_to_www(base, static_root)
        if ok:
            self.stdout.write(self.style.SUCCESS(f'✓ {message}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ {message}'))
