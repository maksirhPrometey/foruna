"""Спільні класи для адмінки контенту."""

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin


class SingletonAdminMixin:
    """Singleton: список → одразу форма редагування."""

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


class PagePreviewMixin:
    """Посилання «Переглянути на сайті» для singleton-сторінок."""

    preview_url_name: str = ''

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if self.preview_url_name:
            fields.append('page_preview')
        return fields

    def page_preview(self, obj):
        if not self.preview_url_name:
            return ''
        from django.urls import reverse
        url = reverse(self.preview_url_name)
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer" '
            'class="font-medium text-primary-600 hover:underline">'
            'Переглянути сторінку на сайті ↗</a>',
            url,
        )

    page_preview.short_description = 'Попередній перегляд'


class ImagePreviewMixin:
    """Превʼю зображення в списку записів."""

    @admin.display(description='Фото')
    def image_preview(self, obj):
        field = getattr(obj, 'image', None) or getattr(obj, 'logo', None)
        if field:
            return format_html(
                '<img src="{}" alt="" class="admin-img-preview">',
                field.url,
            )
        return '—'
