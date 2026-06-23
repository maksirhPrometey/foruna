"""Адмінка singleton-сторінок."""

from unfold.admin import ModelAdmin

from src.content.admin.mixins import PagePreviewMixin, SingletonAdminMixin
from src.content.models import (
    BrandsPage,
    ContactsPage,
    HomePage,
    LabelingPage,
    MarkingPage,
    QualityControlPage,
    SiteConfig,
)


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
    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_title', 'hero_subtitle']}),
        ('Блок «Напрями»', {'fields': ['directions_section_title']}),
        ('Блок «Про компанію»', {
            'fields': ['about_title', 'about_body_1', 'about_body_2', 'about_body_3', 'about_body_4'],
        }),
        ('Цифри на головній', {
            'fields': ['stats'],
            'description': 'Список цифр редагується в розділі «Головна → Цифри».',
        }),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]
    filter_horizontal = ['stats']


class MarkingPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:marking'
    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_direction_label', 'hero_title', 'hero_subtitle']}),
        ('Блок «Чому лазерне маркування»', {'fields': ['intro_title', 'intro_body_1', 'intro_body_2']}),
        ('Продукти', {
            'description': (
                'CIJ, TTO і лазери — у розділі «Маркування» ліворуч '
                '(каплеструйні, термотрансферні, лазерні).'
            ),
            'fields': [],
        }),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]


class QualityControlPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:quality_control'
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
        ('Контент сторінки', {
            'description': (
                'Секції, картки обладнання та галерея FOODMAN — '
                'у розділі «Контроль якості» ліворуч.'
            ),
            'fields': [],
        }),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]


class LabelingPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:labeling'
    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_direction_label', 'hero_title', 'hero_subtitle']}),
        ('Картки на сторінці', {
            'fields': ['products'],
            'description': 'Оберіть активні картки або редагуйте їх у «Картки обладнання».',
        }),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]
    filter_horizontal = ['products']


class ContactsPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:contacts'
    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Текст', {'fields': ['intro_text']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]


class BrandsPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:brands'
    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_title', 'hero_subtitle']}),
        ('Список брендів', {
            'description': 'Картки брендів — у розділі «Бренди → Список брендів».',
            'fields': [],
        }),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]
