"""Латинські slug для моделей каталогу."""

from __future__ import annotations

import re

from django.utils.text import slugify


_ASCII_SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def latin_slug(value: str, *, fallback: str = 'item', max_length: int = 180) -> str:
    """Slug лише a-z, 0-9, дефіс. З кириличного title лишає латиницю/цифри."""
    base = slugify(value or '', allow_unicode=False)
    if not base:
        tokens = re.findall(r'[A-Za-z0-9]+', value or '')
        if tokens:
            base = slugify('-'.join(tokens), allow_unicode=False)
    if not base:
        base = slugify(fallback.replace('_', '-'), allow_unicode=False) or 'item'
    return base[:max_length]


def slug_needs_latin(slug: str) -> bool:
    return not bool(_ASCII_SLUG.fullmatch(slug or ''))


def unique_latin_slug(
    model,
    title: str,
    *,
    category: str = '',
    instance_pk: int | None = None,
    max_length: int = 200,
) -> str:
    """Унікальний латинський slug для запису каталогу."""
    base = latin_slug(title, fallback=category or 'item', max_length=max_length - 12)
    slug = base
    counter = 1

    qs = model.objects.all()
    if instance_pk:
        qs = qs.exclude(pk=instance_pk)

    while qs.filter(slug=slug).exists():
        suffix = f'-{counter}'
        slug = f'{base[: max_length - len(suffix)]}{suffix}'
        counter += 1

    return slug[:max_length]
