"""Автосинхронізація зображень після збереження в адмінці."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from src.content.models_gallery import ProductGalleryImage
from src.content.media_sync import sync_uploaded_content_image
from src.content.models import Brand, LabelingProduct, LaserProduct, QualityProduct
from src.content.models_extra import CIJProduct, GalleryImage, TTOProduct

_IMAGE_FIELDS = {
    CIJProduct: ('image',),
    TTOProduct: ('image',),
    LaserProduct: ('image',),
    QualityProduct: ('image',),
    LabelingProduct: ('image',),
    Brand: ('logo',),
    GalleryImage: ('image',),
    ProductGalleryImage: ('image',),
}


def _connect_image_sync(model, field_names: tuple[str, ...]) -> None:
    @receiver(post_save, sender=model)
    def _sync_images(sender, instance, **kwargs):
        for field_name in field_names:
            field = getattr(instance, field_name, None)
            if field and field.name:
                sync_uploaded_content_image(field.name)


for _model, _fields in _IMAGE_FIELDS.items():
    _connect_image_sync(_model, _fields)
