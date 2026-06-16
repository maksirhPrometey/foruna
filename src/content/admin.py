from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from .models import (
    SiteConfig,
    StatItem,
    LabelingProduct,
    LabelingCategoryContent,
    QualityCategoryContent,
    HomePage,
    MarkingPage,
    QualityControlPage,
    LabelingPage,
    ContactsPage,
    LaserProduct,
    QualityProduct,
    Brand,
    BrandsPage,
    CIJProduct,
    TTOProduct,
)


# ---------------------------------------------------------------------------
# Singleton mixin: changelist → одразу форма редагування
# ---------------------------------------------------------------------------

class _SingletonAdminMixin:
    def changelist_view(self, request, extra_context=None):
        obj = self.model.load()
        url = reverse(
            f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change',
            args=[obj.pk],
        )
        return HttpResponseRedirect(url)

    def has_add_permission(self, request) -> bool:
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


# ---------------------------------------------------------------------------
# Global
# ---------------------------------------------------------------------------

@admin.register(SiteConfig)
class SiteConfigAdmin(_SingletonAdminMixin, ModelAdmin):
    fieldsets = [
        ('Загальне', {'fields': ['company_name', 'tagline']}),
        ('Контакти', {'fields': ['phone_1', 'phone_2', 'email', 'address', 'website']}),
    ]


# ---------------------------------------------------------------------------
# Shared blocks
# ---------------------------------------------------------------------------

@admin.register(StatItem)
class StatItemAdmin(ModelAdmin):
    list_display = ['value', 'label', 'ordering']
    list_editable = ['ordering']


@admin.register(QualityCategoryContent)
class QualityCategoryContentAdmin(ModelAdmin):
    list_display = ['get_category_display', 'section_number', 'section_title', 'ordering']
    list_editable = ['ordering']
    fieldsets = [
        ('Секція', {'fields': ['category', 'section_number', 'section_title', 'ordering']}),
        ('Текст', {'fields': ['body_primary', 'body_secondary']}),
        ('Переваги', {'fields': ['features_label', 'features']}),
    ]


@admin.register(LabelingCategoryContent)
class LabelingCategoryContentAdmin(ModelAdmin):
    list_display = ['get_category_display', 'section_number', 'section_title', 'ordering']
    list_editable = ['ordering']
    fieldsets = [
        ('Секція', {'fields': ['category', 'section_number', 'section_title', 'ordering']}),
        ('Текст', {'fields': ['body_primary', 'body_secondary']}),
        ('Переваги', {'fields': ['features_label', 'features']}),
    ]


@admin.register(LabelingProduct)
class LabelingProductAdmin(ModelAdmin):
    list_display = ['title', 'category', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['category', 'is_active']
    fieldsets = [
        ('Основне', {'fields': ['category', 'title', 'subtitle', 'description', 'image', 'is_active', 'ordering']}),
        ('Характеристики', {'fields': ['features']}),
    ]


# ---------------------------------------------------------------------------
# Page singletons
# ---------------------------------------------------------------------------

@admin.register(HomePage)
class HomePageAdmin(_SingletonAdminMixin, ModelAdmin):
    fieldsets = [
        ('Hero', {'fields': ['hero_title', 'hero_subtitle']}),
        ('Напрями', {'fields': ['directions_section_title']}),
        ('Про компанію', {'fields': ['about_title', 'about_body_1', 'about_body_2']}),
        ('Статистика', {'fields': ['stats']}),
        ('CTA', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]
    filter_horizontal = ['stats']


@admin.register(MarkingPage)
class MarkingPageAdmin(_SingletonAdminMixin, ModelAdmin):
    fieldsets = [
        ('Hero', {'fields': ['hero_direction_label', 'hero_title', 'hero_subtitle']}),
        ('Intro', {'fields': ['intro_title', 'intro_body_1', 'intro_body_2']}),
        ('CTA', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]


@admin.register(QualityControlPage)
class QualityControlPageAdmin(_SingletonAdminMixin, ModelAdmin):
    fieldsets = [
        ('Hero', {'fields': ['hero_direction_label', 'hero_title', 'hero_subtitle']}),
        ('HACCP Intro', {'fields': ['haccp_intro_title', 'haccp_body_1', 'haccp_body_2']}),
        ('CTA', {'fields': ['cta_title', 'cta_body']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]


@admin.register(LabelingPage)
class LabelingPageAdmin(_SingletonAdminMixin, ModelAdmin):
    fieldsets = [
        ('Hero', {'fields': ['hero_direction_label', 'hero_title', 'hero_subtitle']}),
        ('CTA', {'fields': ['cta_title', 'cta_body']}),
        ('Обладнання', {'fields': ['products']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]
    filter_horizontal = ['products']


@admin.register(ContactsPage)
class ContactsPageAdmin(_SingletonAdminMixin, ModelAdmin):
    fieldsets = [
        ('Текст', {'fields': ['intro_text']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]


# ---------------------------------------------------------------------------
# Product catalogs
# ---------------------------------------------------------------------------

@admin.register(LaserProduct)
class LaserProductAdmin(ModelAdmin):
    list_display = ['laser_type', 'title', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['laser_type', 'is_active']
    fieldsets = [
        ('Основне', {'fields': ['laser_type', 'title', 'subtitle', 'description', 'image', 'is_active', 'ordering']}),
        ('Характеристики', {'fields': ['power_range', 'wavelength', 'marking_speed', 'applications']}),
        ('SEO', {'fields': ['meta_description']}),
    ]


@admin.register(QualityProduct)
class QualityProductAdmin(ModelAdmin):
    list_display = ['category', 'title', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['category', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        ('Основне', {'fields': ['category', 'title', 'slug', 'subtitle', 'description', 'image', 'is_active', 'ordering']}),
        ('Деталі', {'fields': ['features']}),
    ]


# ---------------------------------------------------------------------------
# Brands
# ---------------------------------------------------------------------------

@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ['name', 'country', 'founded', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Основне', {'fields': ['name', 'country', 'founded', 'logo', 'website', 'is_active', 'ordering']}),
        ('Контент', {'fields': ['description', 'portfolio']}),
    ]


@admin.register(BrandsPage)
class BrandsPageAdmin(_SingletonAdminMixin, ModelAdmin):
    fieldsets = [
        ('Hero', {'fields': ['hero_title', 'hero_subtitle']}),
        ('SEO', {'fields': ['page_title', 'meta_description']}),
    ]


# ---------------------------------------------------------------------------
# CIJ / TTO
# ---------------------------------------------------------------------------

@admin.register(CIJProduct)
class CIJProductAdmin(ModelAdmin):
    list_display = ['title', 'series', 'model_numbers', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['series', 'is_active']
    fieldsets = [
        ('Основне', {'fields': ['series', 'model_numbers', 'title', 'subtitle', 'image', 'is_active', 'ordering']}),
        ('Контент', {'fields': ['description', 'specs']}),
    ]


@admin.register(TTOProduct)
class TTOProductAdmin(ModelAdmin):
    list_display = ['title', 'model_series', 'print_widths', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Основне', {'fields': ['model_series', 'variants', 'title', 'subtitle', 'image', 'is_active', 'ordering']}),
        ('Контент', {'fields': ['description', 'print_widths', 'specs']}),
    ]
