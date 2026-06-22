"""Імпорт контенту з папки content/ у БД."""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.db import transaction

from src.core.content_data.io import (
    content_paths,
    copy_media_asset,
    copy_static_asset,
    read_json,
)


def _set_image_path(obj, field_name: str, relative: str) -> None:
    if not relative:
        return
    field = getattr(obj, field_name)
    field.name = relative
    obj.save(update_fields=[field_name])


class ContentImporter:
    def __init__(self, content_root: Path, force: bool = False, stdout=None):
        self.root = content_root
        self.force = force
        self.stdout = stdout
        self.paths = content_paths(content_root)
        self.manifest = read_json(self.paths['manifest'])
        self.media_root = Path(settings.MEDIA_ROOT)
        self.static_dir = Path(settings.BASE_DIR) / 'static'

    def _log(self, message: str) -> None:
        if self.stdout:
            self.stdout.write(message)

    def _load(self, filename: str):
        return read_json(self.paths['data'] / filename)

    def _upsert(self, model, lookup: dict, defaults: dict):
        if self.force:
            return model.objects.update_or_create(**lookup, defaults=defaults)
        return model.objects.get_or_create(**lookup, defaults=defaults)

    def _apply_image(self, obj, field: str, relative: str) -> None:
        if not relative:
            return
        if copy_media_asset(self.root, relative, self.media_root):
            _set_image_path(obj, field, relative)
            return
        if self.force or not getattr(obj, field):
            _set_image_path(obj, field, relative)
            self._log(f'  ⚠ файл не знайдено: {relative}')

    def import_all(self) -> None:
        with transaction.atomic():
            for filename in self.manifest['import_order']:
                handler = getattr(self, f'_import_{filename.replace(".json", "")}', None)
                if handler is None:
                    self._log(f'⚠ немає обробника для {filename}')
                    continue
                self._log(f'\n→ {filename}')
                handler()

            self._apply_post_import()

    def _import_site_config(self) -> None:
        from src.content.models import SiteConfig

        data = self._load('site_config.json')
        obj = SiteConfig.load()
        for field, value in data.items():
            setattr(obj, field, value)
        obj.save()
        self._log('  SiteConfig — оновлено')

    def _import_stat_items(self) -> None:
        from src.content.models import StatItem

        self._stat_items = []
        for data in self._load('stat_items.json'):
            obj, created = self._upsert(StatItem, {'label': data['label']}, data)
            self._stat_items.append(obj)
            self._log(f'  {obj.value} — {"створено" if created else "OK"}')

    def _import_home_page(self) -> None:
        from src.content.models import HomePage

        data = self._load('home_page.json')
        home = HomePage.load()
        fields = [k for k in data if hasattr(home, k)]
        for field in fields:
            setattr(home, field, data[field])
        home.save(update_fields=fields)
        if getattr(self, '_stat_items', None) and self.manifest.get('post_import', {}).get('link_home_stats'):
            home.stats.set(self._stat_items)
        self._log('  HomePage — оновлено')

    def _import_page_singleton(self, model, filename: str) -> None:
        data = self._load(filename)
        obj = model.load()
        fields = [k for k in data if hasattr(obj, k)]
        for field in fields:
            setattr(obj, field, data[field])
        obj.save(update_fields=fields)
        self._log(f'  {model.__name__} — оновлено')

    def _import_marking_page(self) -> None:
        from src.content.models import MarkingPage

        self._import_page_singleton(MarkingPage, 'marking_page.json')

    def _import_quality_control_page(self) -> None:
        from src.content.models import QualityControlPage

        self._import_page_singleton(QualityControlPage, 'quality_control_page.json')

    def _import_labeling_page(self) -> None:
        from src.content.models import LabelingPage

        self._import_page_singleton(LabelingPage, 'labeling_page.json')

    def _import_contacts_page(self) -> None:
        from src.content.models import ContactsPage

        self._import_page_singleton(ContactsPage, 'contacts_page.json')

    def _import_brands_page(self) -> None:
        from src.content.models import BrandsPage

        self._import_page_singleton(BrandsPage, 'brands_page.json')

    def _import_laser_products(self) -> None:
        from src.content.models import LaserProduct

        for data in self._load('laser_products.json'):
            image = data.pop('image', '')
            lookup = {'laser_type': data['laser_type']}
            defaults = {k: v for k, v in data.items() if k != 'laser_type'}
            obj, _ = self._upsert(LaserProduct, lookup, defaults)
            self._apply_image(obj, 'image', image)
            self._log(f'  [{data["laser_type"]}] {obj.title}')

    def _import_quality_category_sections(self) -> None:
        from src.content.models import QualityCategoryContent

        for data in self._load('quality_category_sections.json'):
            lookup = {'category': data['category']}
            defaults = {k: v for k, v in data.items() if k != 'category'}
            obj, _ = self._upsert(QualityCategoryContent, lookup, defaults)
            self._log(f'  [{data["category"]}] {obj.section_title}')

    def _import_quality_products(self) -> None:
        from src.content.models import QualityProduct

        for data in self._load('quality_products.json'):
            image = data.pop('image', '')
            lookup = {'title': data['title']}
            defaults = {k: v for k, v in data.items() if k != 'title'}
            obj, _ = self._upsert(QualityProduct, lookup, defaults)
            self._apply_image(obj, 'image', image)
            self._log(f'  {obj.title[:60]}')

    def _import_labeling_category_sections(self) -> None:
        from src.content.models import LabelingCategoryContent

        for data in self._load('labeling_category_sections.json'):
            lookup = {'category': data['category']}
            defaults = {k: v for k, v in data.items() if k != 'category'}
            obj, _ = self._upsert(LabelingCategoryContent, lookup, defaults)
            self._log(f'  [{data["category"]}] {obj.section_title}')

    def _import_labeling_products(self) -> None:
        from src.content.models import LabelingProduct

        for data in self._load('labeling_products.json'):
            row = dict(data)
            image = row.pop('image', '')
            lookup = {'title': row['title']}
            defaults = {k: v for k, v in row.items() if k != 'title'}
            obj, _ = self._upsert(LabelingProduct, lookup, defaults)
            self._apply_image(obj, 'image', image)
            self._log(f'  [{row["category"]}] {obj.title[:55]}')

    def _import_brands(self) -> None:
        from src.content.models import Brand

        for data in self._load('brands.json'):
            row = dict(data)
            logo = row.pop('logo', '')
            lookup = {'name': row['name']}
            defaults = {k: v for k, v in row.items() if k != 'name'}
            obj, _ = self._upsert(Brand, lookup, defaults)
            self._apply_image(obj, 'logo', logo)
            self._log(f'  {obj.name}')

    def _import_cij_products(self) -> None:
        from src.content.models_extra import CIJProduct

        for data in self._load('cij_products.json'):
            row = dict(data)
            image = row.pop('image', '')
            lookup = {'series': row['series']}
            defaults = {k: v for k, v in row.items() if k != 'series'}
            obj, _ = self._upsert(CIJProduct, lookup, defaults)
            self._apply_image(obj, 'image', image)
            self._log(f'  [{row["series"]}] {obj.title[:50]}')

    def _import_tto_products(self) -> None:
        from src.content.models_extra import TTOProduct

        for data in self._load('tto_products.json'):
            row = dict(data)
            image = row.pop('image', '')
            lookup = {'model_series': row['model_series']}
            defaults = {k: v for k, v in row.items() if k != 'model_series'}
            obj, _ = self._upsert(TTOProduct, lookup, defaults)
            self._apply_image(obj, 'image', image)
            self._log(f'  [{row["model_series"]}] {obj.title[:50]}')

    def _import_brochures(self) -> None:
        for item in self._load('brochures.json'):
            static_path = item['static_path']
            if copy_static_asset(self.root, static_path, self.static_dir):
                self._log(f'  ✓ {static_path}')
            else:
                self._log(f'  ⚠ PDF не знайдено: {static_path}')

    def _apply_post_import(self) -> None:
        post = self.manifest.get('post_import', {})
        from src.content.models import (
            HomePage,
            LabelingPage,
            LabelingProduct,
            QualityCategoryContent,
            QualityProduct,
        )

        for rule in post.get('deactivate_quality_products', []):
            qs = QualityProduct.objects.filter(category=rule['category'])
            if rule.get('title_contains'):
                qs = qs.filter(title__icontains=rule['title_contains'])
            count = qs.update(is_active=False)
            if count:
                self._log(f'\n  деактивовано {count} запис(ів) QC')

        for rule in post.get('quality_section_updates', []):
            QualityCategoryContent.objects.filter(category=rule['category']).update(
                **rule.get('fields', {}),
            )

        if post.get('link_labeling_page_products'):
            page = LabelingPage.load()
            products = LabelingProduct.objects.filter(is_active=True)
            page.products.set(products)
            self._log(f'  LabelingPage.products → {products.count()}')

        if post.get('link_home_stats') and getattr(self, '_stat_items', None):
            HomePage.load().stats.set(self._stat_items)


def import_content(content_dir: Path | None = None, force: bool = False, stdout=None) -> None:
    root = content_dir or (Path(settings.BASE_DIR) / 'content')
    if not (root / 'manifest.json').is_file():
        raise FileNotFoundError(f'Не знайдено manifest.json у {root}')
    ContentImporter(root, force=force, stdout=stdout).import_all()
