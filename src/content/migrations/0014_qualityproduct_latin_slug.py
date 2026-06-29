"""Латинські slug для QualityProduct."""

import re

from django.db import migrations, models
from django.utils.text import slugify


_ASCII_SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def _latin_slug(value: str, *, fallback: str, max_length: int = 180) -> str:
    base = slugify(value or '', allow_unicode=False)
    if not base:
        tokens = re.findall(r'[A-Za-z0-9]+', value or '')
        if tokens:
            base = slugify('-'.join(tokens), allow_unicode=False)
    if not base:
        base = slugify(fallback.replace('_', '-'), allow_unicode=False) or 'item'
    return base[:max_length]


def _unique_slug(model, title: str, *, category: str, pk: int) -> str:
    base = _latin_slug(title, fallback=category, max_length=188)
    slug = base
    counter = 1
    qs = model.objects.exclude(pk=pk)
    while qs.filter(slug=slug).exists():
        suffix = f'-{counter}'
        slug = f'{base[:200 - len(suffix)]}{suffix}'
        counter += 1
    return slug[:200]


def latinize_quality_slugs(apps, schema_editor):
    QualityProduct = apps.get_model('content', 'QualityProduct')
    for product in QualityProduct.objects.all().order_by('pk'):
        if product.slug and _ASCII_SLUG.fullmatch(product.slug):
            continue
        product.slug = _unique_slug(
            QualityProduct,
            product.title,
            category=product.category,
            pk=product.pk,
        )
        product.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0013_product_gallery_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualityproduct',
            name='slug',
            field=models.SlugField(
                blank=True,
                max_length=200,
                unique=True,
                verbose_name='Slug (латиниця, автоматично)',
            ),
        ),
        migrations.RunPython(latinize_quality_slugs, migrations.RunPython.noop),
    ]
