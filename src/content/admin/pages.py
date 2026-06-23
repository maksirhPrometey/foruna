"""Адмінка singleton-сторінок."""

from unfold.admin import ModelAdmin

from src.content.admin.links import admin_content_hub
from src.content.admin.mixins import PagePreviewMixin, SingletonAdminMixin
from src.content.admin.sections import LabelingSection, MarkingSection, QualitySection
from src.content.models import (
    Brand,
    BrandsPage,
    ContactsPage,
    HomePage,
    LabelingPage,
    MarkingPage,
    QualityControlPage,
    SiteConfig,
    StatItem,
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
    related_admin_link_fields = ('links_stats',)

    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_title', 'hero_subtitle']}),
        ('Блок «Напрями»', {'fields': ['directions_section_title']}),
        ('Блок «Про компанію»', {
            'fields': ['about_title', 'about_body_1', 'about_body_2', 'about_body_3', 'about_body_4'],
        }),
        ('Цифри на головній (25+, HACCP…)', {'fields': ['stats', 'links_stats']}),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]
    filter_horizontal = ['stats']

    def links_stats(self, obj):
        return admin_content_hub(StatItem, add_label='Додати цифру')

    links_stats.short_description = 'Редагування цифр'


class MarkingPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:marking'
    related_admin_link_fields = ('links_sections',)

    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_direction_label', 'hero_title', 'hero_subtitle']}),
        ('Блок «Чому лазерне маркування»', {'fields': ['intro_title', 'intro_body_1', 'intro_body_2']}),
        ('Розділи та картки на сторінці', {'fields': ['links_sections']}),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]

    def links_sections(self, obj):
        return admin_content_hub(MarkingSection, add_label='Додати розділ')

    links_sections.short_description = 'Розділи (CIJ, TTO, лазери, нові…)'


class QualityControlPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:quality_control'
    related_admin_link_fields = ('links_sections',)

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
        ('Розділи та картки на сторінці', {'fields': ['links_sections']}),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]

    def links_sections(self, obj):
        return admin_content_hub(QualitySection, add_label='Додати розділ')

    links_sections.short_description = 'Розділи (металодетектори, рентген, чеквейери…)'


class LabelingPageAdmin(PagePreviewMixin, SingletonAdminMixin, ModelAdmin):
    preview_url_name = 'core:labeling'
    related_admin_link_fields = ('links_sections',)

    fieldsets = [
        ('Попередній перегляд', {'fields': ['page_preview']}),
        ('Верхній блок (Hero)', {'fields': ['hero_direction_label', 'hero_title', 'hero_subtitle']}),
        ('Розділи та картки на сторінці', {'fields': ['links_sections']}),
        ('Форма внизу (CTA)', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]

    def links_sections(self, obj):
        return admin_content_hub(LabelingSection, add_label='Додати розділ')

    links_sections.short_description = 'Розділи (ALstep, ALritma, Print&Apply…)'


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
