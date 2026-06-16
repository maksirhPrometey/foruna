"""
Генерує placeholder-зображення та прив'язує їх до всіх продуктів.

Запуск:
    python manage.py seed_images
    python manage.py seed_images --force   # перезаписати існуючі
"""
import io
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

# (r, g, b) за типом
PALETTE = {
    # Лазери
    'uv':    (120, 80,  180),
    'co2':   (60,  130, 190),
    'fiber': (40,  150, 100),
    # Контроль якості
    'metal_detector': (80,  110, 160),
    'xray':           (50,  90,  140),
    'checkweigher':   (90,  140, 100),
    'filling':        (60,  120, 150),
    # Бренди
    'brand':          (160, 140, 100),
    # Дефолт
    'default':        (120, 120, 120),
}

LABEL_SIZE = {
    'product': (800, 600),
    'brand':   (400, 200),
}


def _make_image(label: str, color: tuple, size: tuple) -> bytes:
    """Генерує PNG через Pillow з кольоровим фоном і текстом."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)

    # Тонка рамка
    w, h = size
    draw.rectangle([4, 4, w - 5, h - 5], outline=(255, 255, 255), width=2)

    # Текст
    font_size = max(18, min(36, w // (max(len(label), 1))))
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((w - tw) // 2, (h - th) // 2), label, fill=(255, 255, 255), font=font)

    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85)
    return buf.getvalue()


def _attach(obj, field_name: str, filename: str, data: bytes, force: bool) -> bool:
    """Зберігає зображення у поле моделі. Повертає True якщо збережено."""
    field = getattr(obj, field_name)
    if field and not force:
        return False
    cf = ContentFile(data, name=filename)
    field.save(filename, cf, save=True)
    return True


class Command(BaseCommand):
    help = 'Генерує placeholder-зображення для продуктів і брендів'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true',
                            help='Перезаписати існуючі зображення')

    def handle(self, *args, **options):
        force = options['force']

        from src.content.models import LaserProduct, QualityProduct, LabelingProduct, Brand

        self.stdout.write(self.style.MIGRATE_HEADING(
            '=== seed_images: генерація placeholder-зображень ==='))

        total = 0
        total += self._seed_lasers(LaserProduct, force)
        total += self._seed_quality(QualityProduct, force)
        total += self._seed_labeling(LabelingProduct, force)
        total += self._seed_brands(Brand, force)

        self.stdout.write(self.style.SUCCESS(f'\n✓ Готово. Збережено/оновлено: {total} зображень.'))

    def _seed_lasers(self, model, force: bool) -> int:
        self.stdout.write('\n[1/4] Лазерні маркіратори...')
        count = 0
        for obj in model.objects.all():
            color = PALETTE.get(obj.laser_type, PALETTE['default'])
            label = f'{obj.get_laser_type_display()}\n{obj.title}'
            data = _make_image(label, color, LABEL_SIZE['product'])
            filename = f'lasers/{obj.laser_type}_laser.jpg'
            saved = _attach(obj, 'image', filename, data, force)
            status = 'збережено' if saved else 'вже є — пропущено'
            self.stdout.write(f'  {obj} — {status}')
            if saved:
                count += 1
        return count

    def _seed_quality(self, model, force: bool) -> int:
        self.stdout.write('\n[2/4] Контроль якості...')
        count = 0
        for obj in model.objects.all():
            color = PALETTE.get(obj.category, PALETTE['default'])
            label = f'{obj.get_category_display()}\n{obj.title[:40]}'
            data = _make_image(label, color, LABEL_SIZE['product'])
            slug = obj.slug or f'{obj.category}_{obj.pk}'
            filename = f'quality/{slug}.jpg'
            saved = _attach(obj, 'image', filename, data, force)
            status = 'збережено' if saved else 'вже є — пропущено'
            self.stdout.write(f'  {obj.title[:55]} — {status}')
            if saved:
                count += 1
        return count

    def _seed_labeling(self, model, force: bool) -> int:
        self.stdout.write('\n[3/4] Обладнання для етикетування...')
        count = 0
        for obj in model.objects.all():
            color = PALETTE.get('default')
            label = f'{obj.get_category_display()}\n{obj.title[:40]}'
            data = _make_image(label, color, LABEL_SIZE['product'])
            safe_title = obj.title[:30].replace(' ', '_').replace('/', '_')
            filename = f'labeling/{obj.category}_{obj.pk}_{safe_title}.jpg'
            saved = _attach(obj, 'image', filename, data, force)
            status = 'збережено' if saved else 'вже є — пропущено'
            self.stdout.write(f'  [{obj.category}] {obj.title[:50]} — {status}')
            if saved:
                count += 1
        return count

    def _seed_brands(self, model, force: bool) -> int:
        self.stdout.write('\n[4/4] Логотипи брендів...')
        count = 0
        for obj in model.objects.all():
            color = PALETTE['brand']
            label = obj.name
            data = _make_image(label, color, LABEL_SIZE['brand'])
            safe_name = obj.name.replace(' ', '_').lower()
            filename = f'brands/{safe_name}_logo.jpg'
            saved = _attach(obj, 'logo', filename, data, force)
            status = 'збережено' if saved else 'вже є — пропущено'
            self.stdout.write(f'  {obj.name} — {status}')
            if saved:
                count += 1
        return count
