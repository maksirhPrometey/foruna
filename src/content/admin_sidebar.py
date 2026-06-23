"""Навігація Unfold — згруповано за сторінками сайту."""

from django.urls import reverse_lazy

ADMIN_SIDEBAR = {
    'show_search': True,
    'command_search': True,
    'show_all_applications': False,
    'navigation': [
        {
            'title': 'Загальне',
            'items': [
                {
                    'title': 'Контакти та назва сайту',
                    'icon': 'tune',
                    'link': reverse_lazy('admin:content_siteconfig_changelist'),
                },
                {
                    'title': 'Заявки з форм',
                    'icon': 'inbox',
                    'link': reverse_lazy('admin:leads_lead_changelist'),
                },
            ],
        },
        {
            'title': 'Головна',
            'items': [
                {
                    'title': 'Тексти сторінки',
                    'icon': 'home',
                    'link': reverse_lazy('admin:content_homepage_changelist'),
                },
                {
                    'title': 'Цифри (25+, HACCP…)',
                    'icon': 'bar_chart',
                    'link': reverse_lazy('admin:content_statitem_changelist'),
                },
            ],
        },
        {
            'title': 'Маркування',
            'items': [
                {
                    'title': 'Тексти сторінки',
                    'icon': 'edit',
                    'link': reverse_lazy('admin:content_markingpage_changelist'),
                },
                {
                    'title': 'Розділи та картки',
                    'icon': 'view_list',
                    'link': reverse_lazy('admin:content_markingsection_changelist'),
                },
            ],
        },
        {
            'title': 'Контроль якості',
            'items': [
                {
                    'title': 'Тексти сторінки',
                    'icon': 'verified',
                    'link': reverse_lazy('admin:content_qualitycontrolpage_changelist'),
                },
                {
                    'title': 'Розділи та картки',
                    'icon': 'view_list',
                    'link': reverse_lazy('admin:content_qualitysection_changelist'),
                },
            ],
        },
        {
            'title': 'Етикетування',
            'items': [
                {
                    'title': 'Тексти сторінки',
                    'icon': 'label',
                    'link': reverse_lazy('admin:content_labelingpage_changelist'),
                },
                {
                    'title': 'Розділи та картки',
                    'icon': 'view_list',
                    'link': reverse_lazy('admin:content_labelingsection_changelist'),
                },
            ],
        },
        {
            'title': 'Бренди',
            'items': [
                {
                    'title': 'Тексти сторінки',
                    'icon': 'verified_user',
                    'link': reverse_lazy('admin:content_brandspage_changelist'),
                },
                {
                    'title': 'Список брендів',
                    'icon': 'business',
                    'link': reverse_lazy('admin:content_brand_changelist'),
                },
            ],
        },
        {
            'title': 'Контакти',
            'items': [
                {
                    'title': 'Тексти сторінки',
                    'icon': 'contact_phone',
                    'link': reverse_lazy('admin:content_contactspage_changelist'),
                },
            ],
        },
    ],
}
