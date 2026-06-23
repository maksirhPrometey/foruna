"""Адмінка singleton-сторінок."""

from unfold.admin import ModelAdmin

from src.content.admin.links import admin_content_hub
from src.content.admin.mixins import PagePreviewMixin, SingletonAdminMixin
from src.content.models import (
    Brand,
    BrandsPage,
    ContactsPage,
    HomePage,
    LabelingCategoryContent,
    LabelingPage,
    LabelingProduct,
    LaserProduct,
    MarkingPage,
    QualityCategoryContent,
    QualityControlPage,
    QualityProduct,
    SiteConfig,
    StatItem,
)
from src.content.models_extra import CIJProduct, GalleryImage, TTOProduct


class SiteConfigAdmin(SingletonAdminMixin, ModelAdmin):
    fieldsets = [
        ('Загальне', {'fields': ['company_name', 'tagline']}),
        ('Контакти', {
            'fields': [
                'phone_1', 'phone_2', 'email', 'website',
                'address', 'street_address', 'city', 'postal_code',
            ],
        }),
    ]


class HomePageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:home'
    related_admin_link_fields = ('links_stats', 'links_lasers')

    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_title', 'hero_subtitle']}),
        ('Блок «Напрями»', {'fields': ['directions_section_title']}),
        ('Блок «Про компанію»', {
            'fields': ['about_title', 'about_body_1', 'about_body_2', 'about_body_3', 'about_body_4'],
        }),
        ('Цифри на головній (25+, HACCP…)', {
            'fields': ['stats', 'links_stats'],
            'description': 'Оберіть цифри нижче або відредагуйте їх у списку.',
        }),
        ('Лазери в блоці напрямів', {'fields': ['links_lasers']}),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]
    filter_horizontal = ['stats']

    def links_stats(self, obj):
        return admin_content_hub(StatItem, add_label='Додати цифру')

    links_stats.short_description = 'Редагування цифр'

    def links_lasers(self, obj):
        return admin_content_hub(
            LaserProduct,
            add_label='Додати лазер',
            queryset=LaserProduct.objects.filter(is_active=True),
        )

    links_lasers.short_description = 'Картки лазерів (напрям «Маркування»)'


class MarkingPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:marking'
    related_admin_link_fields = ('links_cij', 'links_tto', 'links_lasers')

    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_direction_label', 'hero_title', 'hero_subtitle']}),
        ('Блок «Чому лазерне маркування»', {'fields': ['intro_title', 'intro_body_1', 'intro_body_2']}),
        ('Картки — каплеструйні Linx (CIJ)', {'fields': ['links_cij']}),
        ('Картки — термотрансферні Linx (TTO)', {'fields': ['links_tto']}),
        ('Картки — лазерні маркіратори', {'fields': ['links_lasers']}),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]

    def links_cij(self, obj):
        return admin_content_hub(CIJProduct, add_label='Додати CIJ-маркіратор')

    links_cij.short_description = 'Каплеструйні маркіратори на сторінці'

    def links_tto(self, obj):
        return admin_content_hub(TTOProduct, add_label='Додати TTO-маркіратор')

    links_tto.short_description = 'Термотрансферні маркіратори на сторінці'

    def links_lasers(self, obj):
        return admin_content_hub(LaserProduct, add_label='Додати лазер')

    links_lasers.short_description = 'Лазерні маркіратори на сторінці'


class QualityControlPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:quality_control'
    related_admin_link_fields = (
        'links_sections', 'links_products', 'links_gallery',
    )

    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_direction_label', 'hero_title', 'hero_subtitle']}),
        ('Блок HACCP', {'fields': ['haccp_intro_title', 'haccp_body_1', 'haccp_body_2']}),
        ('Розділ «Контроль розливу» — додаткові блоки', {
            'fields': [
                'filling_extra_1_title', 'filling_extra_1_body', 'filling_extra_1_features',
                'filling_extra_2_title', 'filling_extra_2_body',
            ],
        }),
        ('Тексти секцій (металодетектори, рентген, чеквейери…)', {'fields': ['links_sections']}),
        ('Картки обладнання', {'fields': ['links_products']}),
        ('Галерея FOODMAN (рентген)', {'fields': ['links_gallery']}),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]

    def links_sections(self, obj):
        return admin_content_hub(
            QualityCategoryContent,
            add_label='Додати секцію',
        )

    links_sections.short_description = 'Секції сторінки'

    def links_products(self, obj):
        return admin_content_hub(
            QualityProduct,
            add_label='Додати картку обладнання',
        )

    links_products.short_description = 'Картки обладнання'

    def links_gallery(self, obj):
        return admin_content_hub(
            GalleryImage,
            add_label='Додати фото',
            queryset=GalleryImage.objects.filter(gallery='xray_foodman'),
        )

    links_gallery.short_description = 'Фото галереї FOODMAN'


class LabelingPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:labeling'
    related_admin_link_fields = ('links_sections', 'links_products')

    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_direction_label', 'hero_title', 'hero_subtitle']}),
        ('Тексти секцій', {'fields': ['links_sections']}),
        ('Картки обладнання на сторінці', {
            'fields': ['products', 'links_products'],
            'description': 'Оберіть картки для показу або редагуйте їх у списку нижче.',
        }),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]
    filter_horizontal = ['products']

    def links_sections(self, obj):
        return admin_content_hub(
            LabelingCategoryContent,
            add_label='Додати секцію',
        )

    links_sections.short_description = 'Секції сторінки'

    def links_products(self, obj):
        return admin_content_hub(
            LabelingProduct,
            add_label='Додати картку',
        )

    links_products.short_description = 'Картки обладнання'


class ContactsPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:contacts'
    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Текст', {'fields': ['intro_text']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]


class BrandsPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:brands'
    related_admin_link_fields = ('links_brands',)

    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_title', 'hero_subtitle']}),
        ('Картки брендів', {'fields': ['links_brands']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]

    def links_brands(self, obj):
        return admin_content_hub(Brand, add_label='Додати бренд')

    links_brands.short_description = 'Бренди на сторінці'
