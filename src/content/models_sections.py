"""Універсальні розділи та картки для сторінок сайту."""

from __future__ import annotations

from django.db import models
from django.utils.text import slugify


class ContentSection(models.Model):
    """Розділ сторінки (наприклад «Каплеструйні маркіратори»)."""

    class SitePage(models.TextChoices):
        MARKING = 'marking', 'Маркування'
        QUALITY = 'quality', 'Контроль якості'
        LABELING = 'labeling', 'Етикетування'

    class HeaderStyle(models.TextChoices):
        CATEGORY = 'category', 'Блок категорії (Маркування)'
        NUMBERED = 'numbered', 'Нумерований (КЯ / Етикетування)'
        SIMPLE = 'simple', 'Простий заголовок'

    class Layout(models.TextChoices):
        DETAIL = 'detail', 'Картки детально (фото + текст)'
        GRID = 'grid', 'Сітка карток'
        GALLERY = 'gallery', 'Галерея фото'
        FILLING = 'filling', 'Контроль розливу (КЯ)'
        TEXT = 'text', 'Лише текст (без карток)'

    page = models.CharField('Сторінка', max_length=20, choices=SitePage.choices)
    slug = models.SlugField('Slug (якір на сайті)', max_length=40)
    section_label = models.CharField(
        'Мітка розділу', max_length=80, blank=True,
        help_text='Наприклад: «Напрям 01 — Маркування» або «01»',
    )
    section_number = models.CharField('Номер секції', max_length=10, blank=True)
    title = models.CharField('Заголовок розділу', max_length=160)
    body_primary = models.TextField('Основний текст', blank=True)
    body_secondary = models.TextField('Додатковий текст', blank=True)
    features_label = models.CharField('Заголовок переваг', max_length=160, blank=True)
    features = models.TextField('Переваги (кожна з нового рядка)', blank=True)
    header_style = models.CharField(
        'Стиль заголовка', max_length=20,
        choices=HeaderStyle.choices, default=HeaderStyle.NUMBERED,
    )
    layout = models.CharField(
        'Макет карток', max_length=20,
        choices=Layout.choices, default=Layout.GRID,
    )
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['page', 'ordering']
        verbose_name = 'Розділ сторінки'
        verbose_name_plural = 'Розділи сторінок'
        constraints = [
            models.UniqueConstraint(fields=['page', 'slug'], name='contentsection_page_slug_uniq'),
        ]

    def __str__(self) -> str:
        return f'{self.get_page_display()} — {self.title}'

    def get_features_list(self) -> list[str]:
        return [line.strip() for line in self.features.splitlines() if line.strip()]


class ContentCard(models.Model):
    """Картка обладнання всередині розділу."""

    section = models.ForeignKey(
        ContentSection, on_delete=models.CASCADE,
        related_name='cards', verbose_name='Розділ',
    )
    card_label = models.CharField(
        'Мітка картки', max_length=80, blank=True,
        help_text='Наприклад: «Серія 89хх» або «УФ лазер»',
    )
    title = models.CharField('Назва', max_length=160)
    slug = models.SlugField('Slug (якір)', max_length=80, blank=True)
    subtitle = models.CharField('Підзаголовок', max_length=255, blank=True)
    description = models.TextField('Опис', blank=True)
    image = models.ImageField('Зображення', upload_to='content/cards/', blank=True, null=True)
    model_tags = models.CharField(
        'Моделі / теги (через кому)', max_length=255, blank=True,
    )
    variants = models.CharField('Варіанти (через кому)', max_length=255, blank=True)
    print_widths = models.CharField('Ширина друку', max_length=80, blank=True)
    specs = models.TextField('Характеристики (кожна з нового рядка)', blank=True)
    features = models.TextField('Переваги (кожна з нового рядка)', blank=True)
    wavelength = models.CharField('Довжина хвилі', max_length=80, blank=True)
    power_range = models.CharField('Потужність', max_length=80, blank=True)
    marking_speed = models.CharField('Швидкість маркування', max_length=80, blank=True)
    applications = models.TextField('Сфери застосування (кожна з нового рядка)', blank=True)
    laser_type = models.CharField(
        'Тип лазера (uv/co2/fiber)', max_length=10, blank=True,
        help_text='Для PDF-брошури з /static/brochures/lasers/',
    )
    brochure = models.FileField(
        'PDF-брошура', upload_to='brochures/lasers/', blank=True, null=True,
    )
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Картка розділу'
        verbose_name_plural = 'Картки розділів'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title, allow_unicode=True) or 'card'
            self.slug = base[:80]
        super().save(*args, **kwargs)

    def get_category_display(self) -> str:
        return self.card_label

    def get_specs_list(self) -> list[str]:
        return [line.strip() for line in self.specs.splitlines() if line.strip()]

    def get_features_list(self) -> list[str]:
        return [line.strip() for line in self.features.splitlines() if line.strip()]

    def get_model_tags_list(self) -> list[str]:
        return [t.strip() for t in self.model_tags.split(',') if t.strip()]

    def get_variants_list(self) -> list[str]:
        return [v.strip() for v in self.variants.split(',') if v.strip()]

    def get_applications_list(self) -> list[str]:
        return [line.strip() for line in self.applications.splitlines() if line.strip()]
