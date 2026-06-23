"""Контекст розділів сторінок для views."""

from django.db.models import Prefetch

from src.content.models_extra import GalleryImage
from src.content.models_sections import ContentCard, ContentSection


def sections_for_page(page_key: str):
    return ContentSection.objects.filter(
        page=page_key,
        is_active=True,
    ).prefetch_related(
        Prefetch(
            'cards',
            queryset=ContentCard.objects.filter(is_active=True).order_by('ordering'),
        ),
        Prefetch(
            'gallery_images',
            queryset=GalleryImage.objects.order_by('ordering'),
        ),
    ).order_by('ordering')
