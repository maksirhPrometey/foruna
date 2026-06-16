"""
Додаткові моделі для сторінки «Маркування»:
  CIJProduct — каплеструйні маркіратори (LINX CIJ)
  TTOProduct — термотрансферні маркіратори (LINX TTO)
"""

from django.db import models


class CIJProduct(models.Model):
    """Каплеструйний маркіратор (Continuous Inkjet)."""
    SERIES_CHOICES = [
        ('89xx', 'Серія 89хх'),
        ('99xx', 'Серія 99хх'),
    ]
    series = models.CharField('Серія', max_length=10, choices=SERIES_CHOICES, unique=True)
    model_numbers = models.CharField(
        'Моделі (через кому)', max_length=160,
        help_text='Наприклад: Linx 8900, 8920, 8940',
    )
    title = models.CharField('Назва', max_length=160)
    subtitle = models.CharField('Підзаголовок', max_length=255, blank=True)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='marking/cij/', blank=True, null=True)
    specs = models.TextField(
        'Характеристики (кожна з нового рядка)', blank=True,
        help_text='Кожен рядок — окрема характеристика',
    )
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Каплеструйний маркіратор'
        verbose_name_plural = 'Каплеструйні маркіратори'

    def __str__(self) -> str:
        return f'LINX CIJ {self.get_series_display()} — {self.title}'

    def get_specs_list(self) -> list[str]:
        return [line.strip() for line in self.specs.splitlines() if line.strip()]

    def get_model_numbers_list(self) -> list[str]:
        return [m.strip() for m in self.model_numbers.split(',') if m.strip()]


class TTOProduct(models.Model):
    """Термотрансферний маркіратор (Thermal Transfer Overprinter)."""
    model_series = models.CharField(
        'Серія моделі', max_length=20,
        help_text='Наприклад: TT500, TT750, TT1000',
        unique=True,
    )
    variants = models.CharField(
        'Варіанти (через кому)', max_length=255,
        help_text='Наприклад: Linx TT500 RH',
        blank=True,
    )
    title = models.CharField('Назва', max_length=160)
    subtitle = models.CharField('Підзаголовок', max_length=255, blank=True)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='marking/tto/', blank=True, null=True)
    print_widths = models.CharField(
        'Ширина друку (мм)', max_length=60, blank=True,
        help_text='Наприклад: 32 мм, 53 мм',
    )
    specs = models.TextField('Характеристики (кожна з нового рядка)', blank=True)
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Термотрансферний маркіратор'
        verbose_name_plural = 'Термотрансферні маркіратори'

    def __str__(self) -> str:
        return f'LINX {self.model_series} — {self.title}'

    def get_specs_list(self) -> list[str]:
        return [line.strip() for line in self.specs.splitlines() if line.strip()]

    def get_variants_list(self) -> list[str]:
        return [v.strip() for v in self.variants.split(',') if v.strip()]
