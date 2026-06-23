"""Посилання на пов’язаний контент у формах singleton-сторінок."""

from __future__ import annotations

from django.db.models import Model, QuerySet
from django.urls import reverse
from django.utils.html import format_html, format_html_join


def admin_content_hub(
    model: type[Model],
    *,
    add_label: str = 'Додати',
    queryset: QuerySet | None = None,
    max_items: int = 10,
) -> str:
    """Список записів + кнопки «Список» / «Додати» для адмінки."""
    meta = model._meta
    qs = queryset if queryset is not None else model.objects.all()
    if hasattr(qs, 'order_by'):
        qs = qs.order_by('ordering', 'pk')

    changelist = reverse(f'admin:{meta.app_label}_{meta.model_name}_changelist')
    add_url = reverse(f'admin:{meta.app_label}_{meta.model_name}_add')
    count = qs.count()

    rows = []
    for obj in qs[:max_items]:
        change_url = reverse(
            f'admin:{meta.app_label}_{meta.model_name}_change',
            args=[obj.pk],
        )
        status = ''
        if hasattr(obj, 'is_active') and not obj.is_active:
            status = ' <span class="admin-hub__muted">(неактивний)</span>'
        rows.append(format_html(
            '<li class="admin-hub__item">'
            '<a href="{}" class="admin-hub__edit">Редагувати</a> '
            '<span class="admin-hub__title">{}{}</span>'
            '</li>',
            change_url,
            obj,
            status,
        ))

    if count > max_items:
        rows.append(format_html(
            '<li class="admin-hub__item admin-hub__item--more">'
            '<a href="{}">Показати всі {} записів →</a>'
            '</li>',
            changelist,
            count,
        ))

    list_html = (
        format_html_join('', '{}', rows)
        if rows
        else format_html(
            '<p class="admin-hub__empty">Записів ще немає. '
            '<a href="{}">Додати перший →</a></p>',
            add_url,
        )
    )

    return format_html(
        '<div class="admin-hub">'
        '<p class="admin-hub__actions">'
        '<a href="{}" class="admin-hub__btn">Усі записи ({})</a>'
        '<a href="{}" class="admin-hub__btn admin-hub__btn--primary">+ {}</a>'
        '</p>'
        '<ul class="admin-hub__list">{}</ul>'
        '</div>',
        changelist,
        count,
        add_url,
        add_label,
        list_html,
    )
