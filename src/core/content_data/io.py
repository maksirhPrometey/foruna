"""Читання/запис JSON та копіювання assets для content/."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

MANIFEST_FILE = 'manifest.json'
DATA_DIR = 'data'
ASSETS_DIR = 'assets'
MEDIA_ASSETS = 'media'
STATIC_ASSETS = 'static'
STATIC_CONTENT_PREFIX = 'content'


def sync_image_to_static(relative: str, static_dir: Path, source: Path) -> bool:
    """Копіює зображення в static/content/ для віддачі через collectstatic."""
    if not relative or not source.is_file():
        return False
    dst = static_dir / STATIC_CONTENT_PREFIX / relative
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dst)
    return True


def content_paths(root: Path) -> dict[str, Path]:
    return {
        'root': root,
        'manifest': root / MANIFEST_FILE,
        'data': root / DATA_DIR,
        'assets': root / ASSETS_DIR,
        'media': root / ASSETS_DIR / MEDIA_ASSETS,
        'static': root / ASSETS_DIR / STATIC_ASSETS,
    }


def read_json(path: Path) -> Any:
    with path.open(encoding='utf-8') as fh:
        return json.load(fh)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write('\n')


def copy_tree_if_exists(src: Path, dst: Path) -> int:
    """Копіює файли з src у dst, повертає кількість скопійованих."""
    if not src.exists():
        return 0
    copied = 0
    for item in src.rglob('*'):
        if not item.is_file():
            continue
        rel = item.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied += 1
    return copied


def copy_media_asset(content_root: Path, media_relative: str, media_root: Path) -> bool:
    """Копіює один файл з content/assets/media/ у MEDIA_ROOT."""
    if not media_relative:
        return False
    src = content_root / ASSETS_DIR / MEDIA_ASSETS / media_relative
    if not src.is_file():
        return False
    dst = media_root / media_relative
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def copy_static_asset(content_root: Path, static_relative: str, static_dir: Path) -> bool:
    """Копіює один файл з content/assets/static/ у static/."""
    if not static_relative:
        return False
    src = content_root / ASSETS_DIR / STATIC_ASSETS / static_relative
    if not src.is_file():
        return False
    dst = static_dir / static_relative
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def sync_staticfiles_to_www(base_dir: Path, static_root: Path) -> tuple[bool, str]:
    """ADM.TOOLS: nginx часто віддає /static/ з www/staticfiles/, не з кореня проєкту."""
    www_dir = base_dir / 'www'
    if not www_dir.is_dir():
        return False, 'www/ відсутня'
    www_static = www_dir / 'staticfiles'
    www_static.mkdir(parents=True, exist_ok=True)
    copied = 0
    for item in static_root.rglob('*'):
        if not item.is_file():
            continue
        rel = item.relative_to(static_root)
        dst = www_static / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dst)
        copied += 1
    return True, f'www/staticfiles/ ← {copied} файлів'
