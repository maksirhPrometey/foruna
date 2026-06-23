"""Адмінка розділів та карток."""

from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.content.models_sections import ContentCard, ContentSection


class ContentCardInline(TabularInline):
    model = ContentCard
    extra = 1
    fields = ['ordering', 'is_active', 'card_label', 'title', 'subtitle', 'image']
    ordering = ['ordering']
    show_change_link = True


class ContentSectionAdminBase(ModelAdmin):
    list_display = ['title', 'slug', 'layout', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['layout', 'is_active']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ContentCardInline]
    fieldsets = [
        ('Ідентифікація', {'fields': ['slug', 'ordering', 'is_active']}),
        ('Заголовок', {
            'fields': ['header_style', 'section_label', 'section_number', 'title'],
        }),
        ('Тексти розділу', {'fields': ['body_primary', 'body_secondary']}),
        ('Переваги розділу', {'fields': ['features_label', 'features']}),
        ('Відображення', {
            'fields': ['layout'],
            'description': (
                'Детально — фото + текст (CIJ, лазери); Сітка — картки; '
                'Галерея — фото; Контроль розливу — спецмакет КЯ.'
            ),
        }),
    ]


class PageSectionAdminMixin:
    page_key: str = ''

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(page=self.page_key)

    def save_model(self, request, obj, form, change):
        obj.page = self.page_key
        super().save_model(request, obj, form, change)


class MarkingSection(ContentSection):
    class Meta:
        proxy = True
        verbose_name = 'Розділ (Маркування)'
        verbose_name_plural = 'Розділи — Маркування'


class QualitySection(ContentSection):
    class Meta:
        proxy = True
        verbose_name = 'Розділ (Контроль якості)'
        verbose_name_plural = 'Розділи — КЯ'


class LabelingSection(ContentSection):
    class Meta:
        proxy = True
        verbose_name = 'Розділ (Етикетування)'
        verbose_name_plural = 'Розділи — Етикетування'


@admin.register(ContentSection)
class AllContentSectionAdmin(ModelAdmin):
    """Повний список — для autocomplete; у sidebar — proxy-моделі."""
    search_fields = ['title', 'slug']
    list_display = ['page', 'title', 'slug', 'ordering', 'is_active']
    list_filter = ['page']


@admin.register(MarkingSection)
class MarkingSectionAdmin(PageSectionAdminMixin, ContentSectionAdminBase):
    page_key = 'marking'


@admin.register(QualitySection)
class QualitySectionAdmin(PageSectionAdminMixin, ContentSectionAdminBase):
    page_key = 'quality'


@admin.register(LabelingSection)
class LabelingSectionAdmin(PageSectionAdminMixin, ContentSectionAdminBase):
    page_key = 'labeling'


@admin.register(ContentCard)
class ContentCardAdmin(ModelAdmin):
    list_display = ['title', 'section', 'card_label', 'ordering', 'is_active']
    list_editable = ['ordering', 'is_active']
    list_filter = ['section__page', 'is_active']
    search_fields = ['title', 'card_label']
    autocomplete_fields = ['section']
    fieldsets = [
        ('Розділ', {'fields': ['section', 'ordering', 'is_active']}),
        ('Основне', {
            'fields': ['card_label', 'title', 'slug', 'subtitle', 'description', 'image'],
        }),
        ('Моделі та характеристики', {
            'fields': ['model_tags', 'variants', 'print_widths', 'specs', 'features'],
        }),
        ('Лазер / PDF', {
            'fields': [
                'wavelength', 'power_range', 'marking_speed',
                'applications', 'laser_type', 'brochure',
            ],
            'classes': ['collapse'],
        }),
    ]
