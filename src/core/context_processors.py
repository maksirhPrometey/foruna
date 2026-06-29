from pathlib import Path

from django.conf import settings

from src.content.models import SiteConfig

_STATIC_ASSETS = (
    'css/tokens.css',
    'css/typography.css',
    'css/components.css',
    'js/product_carousel.js',
    'js/reveal.js',
    'js/mobile_menu.js',
)


def _static_version() -> str:
    static_dir = Path(settings.BASE_DIR) / 'static'
    stamps = []
    for rel in _STATIC_ASSETS:
        path = static_dir / rel
        try:
            stamps.append(str(int(path.stat().st_mtime)))
        except OSError:
            continue
    return '-'.join(stamps) if stamps else '0'


def site_config(request):
    return {
        'site': SiteConfig.load(),
        'static_version': _static_version(),
    }
