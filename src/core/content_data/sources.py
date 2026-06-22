"""Збір даних контенту з seed-модулів та дефолтів моделей."""

from __future__ import annotations

import importlib
from typing import Any

from django.db import models


def _load_seed_module(name: str):
    return importlib.import_module(f'src.core.management.commands.{name}')


def _find_image(title: str, mapping: dict[str, str]) -> str | None:
    for key, path in mapping.items():
        if key in title:
            return path
    return None


def model_text_defaults(model) -> dict[str, Any]:
    """Текстові поля singleton-моделі (без M2M та файлів)."""
    result: dict[str, Any] = {}
    for field in model._meta.get_fields():
        if field.many_to_many or field.one_to_many:
            continue
        if field.name in ('id', 'pk'):
            continue
        if isinstance(field, (models.ImageField, models.FileField)):
            continue
        default = field.default
        if default is models.fields.NOT_PROVIDED:
            result[field.name] = ''
        elif callable(default):
            result[field.name] = default()
        else:
            result[field.name] = default
    return result


def site_config_defaults() -> dict[str, Any]:
    from src.content.models import SiteConfig

    return {
        'company_name': 'ФортунаПринт',
        'tagline': 'Системи контролю якості · Маркування · Етикетування',
        'phone_1': '+38 050 334 9262',
        'phone_2': '+38 066 424 1553',
        'email': 'info@fortprint.com.ua',
        'address': '02140, Київ, Вишняківська 13а/49',
        'street_address': 'Вишняківська 13а/49',
        'city': 'Київ',
        'postal_code': '02140',
        'website': 'https://www.fortprint.com.ua',
    }


def collect_export_payload() -> dict[str, Any]:
    """Повертає всі JSON-дані для експорту."""
    sp = _load_seed_module('seed_production')
    sm = _load_seed_module('seed_marking')
    smedia = _load_seed_module('seed_media')
    simages = _load_seed_module('seed_images')

    from src.content.models import (
        BrandsPage,
        ContactsPage,
        HomePage,
        LabelingPage,
        MarkingPage,
        QualityControlPage,
    )

    home_defaults = model_text_defaults(HomePage)
    home_defaults.update(sp.HOME_PAGE_TEXT)

    lasers = []
    for item in sp.LASER_PRODUCTS:
        row = dict(item)
        row['image'] = simages.LASER_IMAGES.get(item['laser_type'], '')
        lasers.append(row)

    quality_products = []
    for item in sp.QUALITY_PRODUCTS:
        row = dict(item)
        row['image'] = _find_image(item['title'], simages.QUALITY_IMAGES) or ''
        quality_products.append(row)

    quality_sections = []
    for section in sp.QUALITY_CATEGORY_SECTIONS:
        row = dict(section)
        if row['category'] == 'filling':
            row['body_secondary'] = ''
        quality_sections.append(row)

    brochures = [
        {
            'laser_type': laser_type,
            'static_path': static_path,
            'url_path': f'/static/{static_path}',
        }
        for laser_type, static_path in {
            'uv': 'brochures/lasers/uv-laser.pdf',
            'co2': 'brochures/lasers/co2-laser.pdf',
            'fiber': 'brochures/lasers/fiber-laser.pdf',
        }.items()
    ]

    return {
        'site_config.json': site_config_defaults(),
        'home_page.json': home_defaults,
        'marking_page.json': model_text_defaults(MarkingPage),
        'quality_control_page.json': model_text_defaults(QualityControlPage),
        'labeling_page.json': model_text_defaults(LabelingPage),
        'contacts_page.json': model_text_defaults(ContactsPage),
        'brands_page.json': model_text_defaults(BrandsPage),
        'stat_items.json': list(sp.STAT_ITEMS),
        'laser_products.json': lasers,
        'quality_category_sections.json': quality_sections,
        'quality_products.json': quality_products,
        'labeling_category_sections.json': list(sp.LABELING_CATEGORY_SECTIONS),
        'labeling_products.json': list(smedia.LABELING_PRODUCTS),
        'brands.json': [
            {**brand, 'logo': smedia.BRAND_LOGOS.get(brand['name'], '')}
            for brand in sp.BRANDS
        ],
        'cij_products.json': list(sm.CIJ_DATA),
        'tto_products.json': list(sm.TTO_DATA),
        'brochures.json': brochures,
        'media_bindings.json': {
            'lasers': simages.LASER_IMAGES,
            'quality_by_title_contains': simages.QUALITY_IMAGES,
            'labeling_by_title_contains': simages.LABELING_IMAGES,
            'brand_logos': simages.BRAND_IMAGES,
        },
    }


def manifest_template() -> dict[str, Any]:
    return {
        'version': 1,
        'description': (
            'Пакет динамічного контенту FortunaPrint. '
            'Тексти — у data/*.json, зображення — assets/media/, PDF — assets/static/. '
            'Імпорт: python manage.py import_content [--dir content] [--force]'
        ),
        'import_order': [
            'site_config.json',
            'stat_items.json',
            'home_page.json',
            'marking_page.json',
            'quality_control_page.json',
            'labeling_page.json',
            'contacts_page.json',
            'brands_page.json',
            'laser_products.json',
            'quality_category_sections.json',
            'quality_products.json',
            'labeling_category_sections.json',
            'labeling_products.json',
            'brands.json',
            'cij_products.json',
            'tto_products.json',
            'brochures.json',
        ],
        'assets': {
            'media': 'assets/media',
            'static': 'assets/static',
        },
        'post_import': {
            'deactivate_quality_products': [
                {'category': 'xray', 'title_contains': 'рівень наливу'},
            ],
            'quality_section_updates': [
                {'category': 'filling', 'fields': {'body_secondary': ''}},
            ],
            'link_labeling_page_products': True,
            'link_home_stats': True,
        },
    }
