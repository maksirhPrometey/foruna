"""Реєстрація адмінки контенту FortunaPrint."""

from django.contrib import admin

from . import catalogs  # noqa: F401
from .pages import (
    BrandsPageAdmin,
    ContactsPageAdmin,
    HomePageAdmin,
    LabelingPageAdmin,
    MarkingPageAdmin,
    QualityControlPageAdmin,
    SiteConfigAdmin,
)
from src.content.models import (
    BrandsPage,
    ContactsPage,
    HomePage,
    LabelingPage,
    MarkingPage,
    QualityControlPage,
    SiteConfig,
)

admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(MarkingPage, MarkingPageAdmin)
admin.site.register(QualityControlPage, QualityControlPageAdmin)
admin.site.register(LabelingPage, LabelingPageAdmin)
admin.site.register(ContactsPage, ContactsPageAdmin)
admin.site.register(BrandsPage, BrandsPageAdmin)
