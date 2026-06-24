from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from pathlib import Path

register = template.Library()

LASER_BROCHURE_STATIC = {
    'uv': 'brochures/lasers/uv-laser.pdf',
    'co2': 'brochures/lasers/co2-laser.pdf',
    'fiber': 'brochures/lasers/fiber-laser.pdf',
}


@register.simple_tag(takes_context=True)
def active_nav(context, url_name):
    request = context.get('request')
    if not request:
        return ''
    return 'is-active' if request.resolver_match and request.resolver_match.url_name == url_name else ''


def _ideal_cols(count: int, max_cols: int = 3) -> int:
    """Return the largest divisor of count that is <= max_cols (no orphan cards)."""
    n = max(1, count)
    if n <= max_cols:
        return n
    for c in range(max_cols, 1, -1):
        if n % c == 0:
            return c
    return max_cols


@register.filter(name='ideal_cols')
def ideal_cols_filter(count, max_cols: int = 3) -> int:
    """{{ items|length|ideal_cols:3 }} → integer cols count."""
    try:
        return _ideal_cols(int(count), int(max_cols))
    except (TypeError, ValueError):
        return int(max_cols)


@register.simple_tag
def content_image_url(name: str) -> str:
    """
    URL зображення: /static/content/ якщо файл є, інакше /media/ (свіже upload).
    """
    if not name:
        return ''

    static_rel = f'content/{name}'
    if finders.find(static_rel):
        return static(static_rel)

    static_root_file = Path(settings.STATIC_ROOT) / static_rel
    if static_root_file.is_file():
        return f'{settings.STATIC_URL}{static_rel}'

    media_file = Path(settings.MEDIA_ROOT) / name
    if media_file.is_file():
        return f'{settings.MEDIA_URL}{name}'

    return f'{settings.STATIC_URL}{static_rel}'


@register.simple_tag
def get_product_images(product) -> list[dict[str, str]]:
    """Основне фото + галерея без дублів."""
    if not product:
        return []

    images: list[dict[str, str]] = []
    seen: set[str] = set()
    title = getattr(product, 'title', None) or getattr(product, 'name', '') or ''

    main_field = getattr(product, 'image', None) or getattr(product, 'logo', None)
    if main_field and main_field.name:
        images.append({'path': main_field.name, 'alt': title})
        seen.add(main_field.name)

    gallery = getattr(product, 'gallery_images', None)
    if gallery is not None:
        for item in gallery.all():
            if item.image.name and item.image.name not in seen:
                images.append({
                    'path': item.image.name,
                    'alt': item.alt_text or title,
                })
                seen.add(item.image.name)

    return images


@register.simple_tag
def laser_brochure_url(laser) -> str:
    """URL PDF-брошури для лазерного продукту (upload або static fallback)."""
    laser_type = laser if isinstance(laser, str) else getattr(laser, 'laser_type', '')
    if not isinstance(laser, str):
        brochure = getattr(laser, 'brochure', None)
        if brochure:
            return brochure.url
    path = LASER_BROCHURE_STATIC.get(laser_type)
    if not path or not finders.find(path):
        return ''
    return static(path)
