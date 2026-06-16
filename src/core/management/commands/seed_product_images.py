"""
Призначення зображень до QualityProduct і LaserProduct.

Запуск:
    python manage.py seed_product_images
    python manage.py seed_product_images --force
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


LASER_IMAGES = {
    'uv':    'marking/laser_uv.jpg',
    'co2':   'marking/laser_co2_clean.jpg',
    'fiber': 'marking/laser_fiber_clean.jpg',
}

QUALITY_IMAGES = [
    {
        'category': 'metal_detector',
        'title_contains': 'FMD-3010',
        'image': 'quality/easyweigh_metal_detector.jpg',
    },
    {
        'category': 'metal_detector',
        'title_contains': 'FMD-5015',
        'image': 'quality/easyweigh_metal_detector.jpg',
    },
    {
        'category': 'metal_detector',
        'title_contains': 'FMD-YCW-210',
        'image': 'quality/easyweigh_combi.jpg',
    },
    {
        'category': 'metal_detector',
        'title_contains': 'FMD-YCW-300',
        'image': 'quality/easyweigh_combi.jpg',
    },
    {
        'category': 'xray',
        'title_contains': None,
        'image': 'quality/easyweigh_xray.jpg',
    },
    {
        'category': 'checkweigher',
        'title_contains': None,
        'image': 'quality/easyweigh_checkweigher.jpg',
    },
    {
        'category': 'filling',
        'title_contains': 'T-LINE',
        'image': 'quality/tline_filling.jpg',
    },
    {
        'category': 'filling',
        'title_contains': 'FMS',
        'image': 'quality/tline_fms.jpg',
    },
]


class Command(BaseCommand):
    help = 'Призначення зображень до QualityProduct і LaserProduct'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true',
                            help='Перезаписати існуючі зображення')

    def handle(self, *args, **options):
        force = options['force']
        from src.content.models import QualityProduct, LaserProduct

        self.stdout.write(self.style.MIGRATE_HEADING(
            '=== seed_product_images: зображення лазерів та якості ==='))

        try:
            with transaction.atomic():
                self._seed_laser(LaserProduct, force)
                self._seed_quality(QualityProduct, force)
        except Exception as exc:
            raise CommandError(f'Помилка: {exc}') from exc

        self.stdout.write(self.style.SUCCESS('\n✓ seed_product_images завершено успішно.'))

    def _seed_laser(self, model, force: bool) -> None:
        self.stdout.write('\n[1/2] Лазерні маркіратори...')
        for laser_type, image_path in LASER_IMAGES.items():
            qs = model.objects.filter(laser_type=laser_type)
            for obj in qs:
                if force or not obj.image:
                    obj.image = image_path
                    obj.save(update_fields=['image'])
                    self.stdout.write(f'  [{laser_type}] {obj.title[:50]} → {image_path}')
                else:
                    self.stdout.write(f'  [{laser_type}] вже має зображення, пропуск')

    def _seed_quality(self, model, force: bool) -> None:
        self.stdout.write('\n[2/2] Продукти контролю якості...')
        for rule in QUALITY_IMAGES:
            cat = rule['category']
            title_frag = rule['title_contains']
            image_path = rule['image']

            qs = model.objects.filter(category=cat)
            if title_frag:
                qs = qs.filter(title__icontains=title_frag)

            for obj in qs:
                if force or not obj.image:
                    obj.image = image_path
                    obj.save(update_fields=['image'])
                    self.stdout.write(f'  [{cat}] {obj.title[:50]} → {image_path}')
                else:
                    self.stdout.write(f'  [{cat}] {obj.title[:50]} — вже є зображення')
