"""Синхронізація media/ → static/content/ для всіх зображень каталогу."""

from __future__ import annotations

from django.core.management.base import BaseCommand

from src.content.media_sync import sync_uploaded_content_image
from src.content.models import Brand, LabelingProduct, LaserProduct, QualityProduct
from src.content.models_extra import CIJProduct, GalleryImage, TTOProduct

_MODELS = (
    (CIJProduct, 'image'),
    (TTOProduct, 'image'),
    (LaserProduct, 'image'),
    (QualityProduct, 'image'),
    (LabelingProduct, 'image'),
    (Brand, 'logo'),
    (GalleryImage, 'image'),
)


class Command(BaseCommand):
    help = 'Копіює зображення з media/ у static/content/ (після змін у адмінці)'

    def handle(self, *args, **options):
        synced = 0
        for model, field_name in _MODELS:
            for obj in model.objects.all():
                field = getattr(obj, field_name, None)
                if field and field.name and sync_uploaded_content_image(field.name):
                    synced += 1
                    self.stdout.write(f'  ✓ {field.name}')
        self.stdout.write(self.style.SUCCESS(f'Готово: {synced} файлів'))
