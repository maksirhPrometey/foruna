"""Синхронізація завантажених зображень media/ → static/content/."""

from __future__ import annotations

import shutil
from pathlib import Path

from django.conf import settings

from src.core.content_data.io import STATIC_CONTENT_PREFIX, sync_image_to_static


def sync_uploaded_content_image(relative: str) -> bool:
    """Після upload в адмінці — копіює у static/, staticfiles/, www/staticfiles/."""
    if not relative:
        return False

    source = Path(settings.MEDIA_ROOT) / relative
    if not source.is_file():
        return False

    static_dir = Path(settings.BASE_DIR) / 'static'
    sync_image_to_static(relative, static_dir, source)

    targets = [Path(settings.STATIC_ROOT)]
    www_static = Path(settings.BASE_DIR) / 'www' / 'staticfiles'
    if www_static.parent.is_dir():
        targets.append(www_static)

    for root in targets:
        dst = root / STATIC_CONTENT_PREFIX / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dst)

    return True
