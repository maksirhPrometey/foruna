"""Експорт контенту у папку content/."""

from __future__ import annotations

from pathlib import Path

from django.conf import settings

from src.core.content_data.io import content_paths, copy_tree_if_exists, write_json
from src.core.content_data.sources import collect_export_payload, manifest_template


def _collect_media_paths(payload: dict) -> set[str]:
    paths: set[str] = set()
    for key in (
        'laser_products.json',
        'quality_products.json',
        'labeling_products.json',
        'brands.json',
        'cij_products.json',
        'tto_products.json',
    ):
        for row in payload.get(key, []):
            image = row.get('image') or row.get('logo')
            if image:
                paths.add(image)
    return paths


def _copy_media_files(content_root: Path, relative_paths: set[str]) -> tuple[int, list[str]]:
    media_root = Path(settings.MEDIA_ROOT)
    copied = 0
    missing: list[str] = []
    media_dst = content_root / 'assets' / 'media'
    for rel in sorted(relative_paths):
        src = media_root / rel
        if src.is_file():
            dst = media_dst / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())
            copied += 1
        else:
            missing.append(rel)
    return copied, missing


def export_content(content_dir: Path | None = None) -> dict:
    """Записує JSON + assets у content/. Повертає статистику."""
    root = content_dir or (Path(settings.BASE_DIR) / 'content')
    paths = content_paths(root)
    paths['data'].mkdir(parents=True, exist_ok=True)
    paths['media'].mkdir(parents=True, exist_ok=True)
    paths['static'].mkdir(parents=True, exist_ok=True)

    payload = collect_export_payload()
    for filename, data in payload.items():
        write_json(paths['data'] / filename, data)

    write_json(paths['manifest'], manifest_template())

    static_src = Path(settings.BASE_DIR) / 'static' / 'brochures'
    static_copied = copy_tree_if_exists(static_src, paths['static'] / 'brochures')

    media_paths = _collect_media_paths(payload)
    media_copied, media_missing = _copy_media_files(root, media_paths)

    return {
        'root': str(root),
        'json_files': len(payload) + 1,
        'static_files': static_copied,
        'media_files': media_copied,
        'media_missing': media_missing,
    }
