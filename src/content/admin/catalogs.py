"""Адмінка каталогів, галерей та спільних блоків."""

from django.contrib import admin
from unfold.admin import ModelAdmin

from src.content.admin.mixins import ImagePreviewMixin
from src.content.models import (
    Brand,
    LabelingCategoryContent,
    LabelingProduct,
    LaserProduct,
    QualityCategoryContent,
    QualityProduct,
    StatItem,
)
from src.content.models_extra import CIJProduct, GalleryImage, TTOProduct


class _ImageAdminMixin(ImagePreviewMixin):
    """Превʼю зображення у списку та на формі."""

    readonly_fields = ['image_preview_detail']

    @admin.display(description='Поточне зображення')
    def image_preview_detail(self, obj):
        field = getattr(obj, 'image', None) or getattr(obj, 'logo', None)
        if field:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" alt="" class="admin-img-preview admin-img-preview--detail">',
                field.url,
            )
        return '—'


@admin.register(StatItem)
class StatItemAdmin(ModelAdmin):
    list_display = ['value', 'label', 'ordering']
    list_editable = ['ordering']
    ordering = ['ordering']


@admin.register(QualityCategoryContent)
class QualityCategoryContentAdmin(ModelAdmin):
    list_display = ['get_category_display', 'section_number', 'section_title', 'ordering']
    list_editable = ['ordering']
    list_filter = ['category']
    ordering = ['ordering']
    fieldsets = [
        ('Секція', {'fields': ['category', 'section_number', 'section_title', 'ordering']}),
        ('Текст', {'fields': ['body_primary', 'body_secondary']}),
        ('Переваги', {'fields': ['features_label', 'features']}),
    ]


@admin.register(LabelingCategoryContent)
class LabelingCategoryContentAdmin(ModelAdmin):
    list_display = ['get_category_display', 'section_number', 'section_title', 'ordering']
    list_editable = ['ordering']
    list_filter = ['category']
    ordering = ['ordering']
    fieldsets = [
        ('Секція', {'fields': ['category', 'section_number', 'section_title', 'ordering']}),
        ('Текст', {'fields': ['body_primary', 'body_secondary']}),
        ('Переваги', {'fields': ['features_label', 'features']}),
    ]


@admin.register(LabelingProduct)
class LabelingProductAdmin(_ImageAdminMixin, ModelAdmin):
    list_display = ['image_preview', 'title', 'category', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['category', 'is_active']
    ordering = ['category', 'ordering']
    fieldsets = [
        ('Основне', {
            'fields': [
                'category', 'title', 'subtitle', 'description',
                'image', 'image_preview_detail', 'is_active', 'ordering',
            ],
        }),
        ('Характеристики', {'fields': ['features']}),
    ]


@admin.register(LaserProduct)
class LaserProductAdmin(_ImageAdminMixin, ModelAdmin):
    list_display = ['image_preview', 'laser_type', 'title', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['laser_type', 'is_active']
    ordering = ['ordering']
    fieldsets = [
        ('Основне', {
            'fields': [
                'laser_type', 'title', 'subtitle', 'description',
                'image', 'image_preview_detail', 'is_active', 'ordering',
            ],
        }),
        ('Характеристики', {'fields': ['power_range', 'wavelength', 'marking_speed', 'applications']}),
        ('PDF-брошура', {
            'fields': ['brochure'],
            'description': 'Завантажте PDF або залиште порожнім — використається файл з /static/brochures/lasers/.',
        }),
        ('SEO', {'fields': ['meta_description']}),
    ]


@admin.register(QualityProduct)
class QualityProductAdmin(_ImageAdminMixin, ModelAdmin):
    list_display = ['image_preview', 'category', 'title', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['category', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['category', 'ordering']
    fieldsets = [
        ('Основне', {
            'fields': [
                'category', 'title', 'slug', 'subtitle', 'description',
                'image', 'image_preview_detail', 'is_active', 'ordering',
            ],
        }),
        ('Деталі', {'fields': ['features']}),
    ]


@admin.register(Brand)
class BrandAdmin(_ImageAdminMixin, ModelAdmin):
    list_display = ['image_preview', 'name', 'country', 'founded', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['is_active']
    ordering = ['ordering']

    @admin.display(description='Логотип')
    def image_preview(self, obj):
        return super().image_preview(obj)

    fieldsets = [
        ('Основне', {
            'fields': [
                'name', 'country', 'founded', 'logo', 'image_preview_detail',
                'website', 'is_active', 'ordering',
            ],
        }),
        ('Контент', {'fields': ['description', 'portfolio']}),
    ]


@admin.register(CIJProduct)
class CIJProductAdmin(_ImageAdminMixin, ModelAdmin):
    list_display = ['image_preview', 'title', 'series', 'model_numbers', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['series', 'is_active']
    ordering = ['ordering']
    fieldsets = [
        ('Основне', {
            'fields': [
                'series', 'model_numbers', 'title', 'subtitle',
                'image', 'image_preview_detail', 'is_active', 'ordering',
            ],
        }),
        ('Контент', {'fields': ['description', 'specs']}),
    ]


@admin.register(TTOProduct)
class TTOProductAdmin(_ImageAdminMixin, ModelAdmin):
    list_display = ['image_preview', 'title', 'model_series', 'print_widths', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['is_active']
    ordering = ['ordering']
    fieldsets = [
        ('Основне', {
            'fields': [
                'model_series', 'variants', 'title', 'subtitle',
                'image', 'image_preview_detail', 'is_active', 'ordering',
            ],
        }),
        ('Контент', {'fields': ['description', 'print_widths', 'specs']}),
    ]


@admin.register(GalleryImage)
class GalleryImageAdmin(_ImageAdminMixin, ModelAdmin):
    list_display = ['image_preview', 'gallery', 'alt_text', 'ordering']
    list_editable = ['ordering', 'alt_text']
    list_filter = ['gallery']
    ordering = ['gallery', 'ordering']
    fieldsets = [
        ('Галерея', {'fields': ['section', 'gallery', 'ordering', 'alt_text']}),
        ('Зображення', {'fields': ['image', 'image_preview_detail']}),
    ]
