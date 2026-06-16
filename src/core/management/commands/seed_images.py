"""
Прив'язує реальні зображення до продуктів і брендів.
Якщо файл є в MEDIA_ROOT — просто встановлює шлях.
Якщо немає — генерує кольоровий placeholder через Pillow.

Запуск:
    python manage.py seed_images
    python manage.py seed_images --force   # перезаписати існуючі
"""
import io
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

# ── Маппінг: laser_type → реальний файл у media/ ──────────────────────────────
LASER_IMAGES = {
    'uv':    'marking/laser_uv_clean.jpg',
    'co2':   'marking/laser_co2_clean.jpg',
    'fiber': 'marking/laser_fiber_clean.jpg',
}

# ── Маппінг: QualityProduct.title (substring) → файл ─────────────────────────
# Використовуємо ASCII-назви файлів — надійніші при docker cp
QUALITY_IMAGES = {
    'FMD-3010':    'quality/easyweigh_metal_detector.jpg',
    'FMD-5015':    'quality/easyweigh_metal_detector.jpg',
    'FMD-YCW-210': 'quality/easyweigh_combi.jpg',
    'FMD-YCW-300': 'quality/easyweigh_combi.jpg',
    'FOODMAN (базова': 'quality/easyweigh_xray.jpg',
    'FOODMAN (рівень': 'quality/easyweigh_xray.jpg',
    'YCW-150':     'quality/easyweigh_checkweigher.jpg',
    'YCW-300':     'quality/easyweigh_checkweigher.jpg',
    'T-LINE (базова': 'quality/tline_filling.jpg',
    'FMS':         'quality/tline_fms.jpg',
}

# ── Маппінг: LabelingProduct.title (substring) → файл ────────────────────────
LABELING_IMAGES = {
    'ALstep E':       'labeling/alstep_main.jpg',
    'ALstep S/M':     'labeling/alstep_main.jpg',
    'ALstep T':       'labeling/alstep_t_main.jpg',
    'ALritma S/M/L':  'labeling/alritma_main.jpg',
    'ALritma X':      'labeling/alritma_x_main.jpg',
    'ALritma T':      'labeling/alritma_t_main.jpg',
    'ALcode —':       'labeling/alcode_main.jpg',
    'ALcode LT':      'labeling/alcode_lt_main.jpg',
    'ALcode P':       'labeling/alcode_p_main.jpg',
    'ALline C':       'labeling/alline_c_main.jpg',
    'ALline E':       'labeling/alline_e_main.jpg',
    'ALbelt —':       'labeling/albelt_main.jpg',
    'ALbelt C':       'labeling/albelt_c_main.jpg',
}

# ── Маппінг: Brand.name → файл ───────────────────────────────────────────────
BRAND_IMAGES = {
    'LINX':              'brands/linx_logo.png',
    'ALTECH':            'brands/altech_logo.jpg',
    'Easyweigh FOODMAN': 'brands/easyweigh_logo.png',
    'T-LINE Technology': 'brands/tline_logo.png',
}

# ── Placeholder palette ───────────────────────────────────────────────────────
PALETTE = {
    'uv':    (120, 80,  180),
    'co2':   (60,  130, 190),
    'fiber': (40,  150, 100),
    'metal_detector': (80,  110, 160),
    'xray':           (50,  90,  140),
    'checkweigher':   (90,  140, 100),
    'filling':        (60,  120, 150),
    'brand':          (160, 140, 100),
    'default':        (120, 120, 120),
}


def _real_path(relative: str) -> Path | None:
    """Повертає абсолютний шлях якщо файл існує в MEDIA_ROOT."""
    p = Path(settings.MEDIA_ROOT) / relative
    return p if p.exists() else None


def _set_field_path(obj, field_name: str, relative: str, force: bool) -> bool:
    """Встановлює шлях поля без перезапису файлу."""
    field = getattr(obj, field_name)
    if field and str(field) == relative and not force:
        return False
    field.name = relative
    obj.save(update_fields=[field_name])
    return True


def _make_placeholder(label: str, color: tuple, size=(800, 600)) -> bytes:
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    w, h = size
    draw.rectangle([4, 4, w - 5, h - 5], outline=(255, 255, 255), width=2)
    font_size = max(18, min(36, w // max(len(label), 1)))
    try:
        font = ImageFont.truetype(
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((w - tw) // 2, (h - th) // 2), label, fill=(255, 255, 255), font=font)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85)
    return buf.getvalue()


def _attach_placeholder(obj, field_name: str, filename: str,
                        label: str, color: tuple, force: bool) -> bool:
    field = getattr(obj, field_name)
    if field and not force:
        return False
    data = _make_placeholder(label, color)
    cf = ContentFile(data, name=filename)
    field.save(filename, cf, save=True)
    return True


def _find_mapping(title: str, mapping: dict) -> str | None:
    for key, path in mapping.items():
        if key in title:
            return path
    return None


class Command(BaseCommand):
    help = 'Прив\'язує реальні зображення до продуктів (або генерує placeholder)'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true',
                            help='Перезаписати існуючі зображення')

    def handle(self, *args, **options):
        force = options['force']
        from src.content.models import LaserProduct, QualityProduct, LabelingProduct, Brand

        self.stdout.write(self.style.MIGRATE_HEADING(
            '=== seed_images: прив\'язка реальних зображень ==='))

        total = 0
        total += self._seed_lasers(LaserProduct, force)
        total += self._seed_quality(QualityProduct, force)
        total += self._seed_labeling(LabelingProduct, force)
        total += self._seed_cij_tto(force)
        total += self._seed_brands(Brand, force)

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Готово. Оброблено: {total} зображень.'))

    def _seed_lasers(self, model, force: bool) -> int:
        self.stdout.write('\n[1/4] Лазерні маркіратори...')
        count = 0
        for obj in model.objects.all():
            rel = LASER_IMAGES.get(obj.laser_type)
            if rel and _real_path(rel):
                saved = _set_field_path(obj, 'image', rel, force)
                tag = '✓ реальне' if saved else 'вже є'
            else:
                color = PALETTE.get(obj.laser_type, PALETTE['default'])
                fn = f'lasers/{obj.laser_type}_laser.jpg'
                saved = _attach_placeholder(
                    obj, 'image', fn,
                    f'{obj.get_laser_type_display()}\n{obj.title}',
                    color, force)
                tag = 'placeholder' if saved else 'вже є'
            self.stdout.write(f'  {obj.get_laser_type_display()} — {tag}')
            if saved:
                count += 1
        return count

    def _seed_quality(self, model, force: bool) -> int:
        self.stdout.write('\n[2/4] Контроль якості...')
        count = 0
        for obj in model.objects.all():
            rel = _find_mapping(obj.title, QUALITY_IMAGES)
            if rel and _real_path(rel):
                saved = _set_field_path(obj, 'image', rel, force)
                tag = '✓ реальне' if saved else 'вже є'
            else:
                color = PALETTE.get(obj.category, PALETTE['default'])
                slug = obj.slug or f'{obj.category}_{obj.pk}'
                fn = f'quality/{slug[:60]}.jpg'
                saved = _attach_placeholder(
                    obj, 'image', fn,
                    f'{obj.get_category_display()}\n{obj.title[:40]}',
                    color, force)
                tag = 'placeholder' if saved else 'вже є'
            self.stdout.write(f'  {obj.title[:55]} — {tag}')
            if saved:
                count += 1
        return count

    def _seed_labeling(self, model, force: bool) -> int:
        self.stdout.write('\n[3/4] Обладнання для етикетування...')
        count = 0
        for obj in model.objects.all():
            rel = _find_mapping(obj.title, LABELING_IMAGES)
            if rel and _real_path(rel):
                saved = _set_field_path(obj, 'image', rel, force)
                tag = '✓ реальне' if saved else 'вже є'
            else:
                fn = f'labeling/{obj.category}_{obj.pk}.jpg'
                saved = _attach_placeholder(
                    obj, 'image', fn,
                    f'{obj.get_category_display()}\n{obj.title[:40]}',
                    PALETTE['default'], force)
                tag = 'placeholder' if saved else 'вже є'
            self.stdout.write(f'  [{obj.category}] {obj.title[:50]} — {tag}')
            if saved:
                count += 1
        return count

    def _seed_cij_tto(self, force: bool) -> int:
        from src.content.models_extra import CIJProduct, TTOProduct
        self.stdout.write('\n[5/6] CIJ маркіратори (LINX)...')
        count = 0
        CIJ_IMAGES = {
            '89xx': 'marking/cij/linx_8900.jpg',
            '99xx': 'marking/cij/linx_99xx.jpg',
        }
        for obj in CIJProduct.objects.all():
            rel = CIJ_IMAGES.get(obj.series)
            if rel and _real_path(rel):
                saved = _set_field_path(obj, 'image', rel, force)
                tag = '✓ реальне' if saved else 'вже є'
            else:
                tag = 'файл не знайдено'
                saved = False
            self.stdout.write(f'  {obj.title[:55]} — {tag}')
            if saved:
                count += 1

        self.stdout.write('\n[6/6] TTO маркіратори (LINX)...')
        TTO_IMAGES = {
            'TT500':  'marking/tto/linx_tt500.jpg',
            'TT750':  'marking/tto/linx_tt750.jpg',
            'TT1000': 'marking/tto/linx_tt1000.jpg',
        }
        for obj in TTOProduct.objects.all():
            rel = TTO_IMAGES.get(obj.model_series)
            if rel and _real_path(rel):
                saved = _set_field_path(obj, 'image', rel, force)
                tag = '✓ реальне' if saved else 'вже є'
            else:
                tag = 'файл не знайдено'
                saved = False
            self.stdout.write(f'  {obj.title[:55]} — {tag}')
            if saved:
                count += 1
        return count

    def _seed_brands(self, model, force: bool) -> int:
        self.stdout.write('\n[4/4] Логотипи брендів...')
        count = 0
        for obj in model.objects.all():
            rel = BRAND_IMAGES.get(obj.name)
            if rel and _real_path(rel):
                saved = _set_field_path(obj, 'logo', rel, force)
                tag = '✓ реальне' if saved else 'вже є'
            else:
                fn = f'brands/{obj.name.replace(" ", "_").lower()}_logo.jpg'
                saved = _attach_placeholder(
                    obj, 'logo', fn, obj.name,
                    PALETTE['brand'], force, )
                tag = 'placeholder' if saved else 'вже є'
            self.stdout.write(f'  {obj.name} — {tag}')
            if saved:
                count += 1
        return count
