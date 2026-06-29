"""Додаткові фото для карток каталогу (Generic FK)."""

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ProductGalleryImage(models.Model):
    """Додаткове фото до картки обладнання (основне — поле image/logo)."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField('Зображення', upload_to='catalog/gallery/')
    alt_text = models.CharField('Alt-текст', max_length=160, blank=True)
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['ordering', 'pk']
        verbose_name = 'Додаткове фото'
        verbose_name_plural = 'Додаткові фото'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self) -> str:
        return f'Фото #{self.ordering} — {self.image.name}'

    def save(self, *args, **kwargs):
        if (
            self.ordering == 0
            and self.content_type_id
            and self.object_id
        ):
            siblings = ProductGalleryImage.objects.filter(
                content_type_id=self.content_type_id,
                object_id=self.object_id,
            )
            if self.pk:
                siblings = siblings.exclude(pk=self.pk)
            last = siblings.order_by('-ordering').values_list('ordering', flat=True).first()
            if last is not None:
                self.ordering = last + 1
        super().save(*args, **kwargs)


GALLERY_RELATION = GenericRelation(
    'content.ProductGalleryImage',
    content_type_field='content_type',
    object_id_field='object_id',
)
