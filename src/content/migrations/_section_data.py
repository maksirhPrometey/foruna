"""Міграція даних у ContentSection / ContentCard."""

from __future__ import annotations


def migrate_legacy_sections(apps, schema_editor) -> None:
    ContentSection = apps.get_model('content', 'ContentSection')
    ContentCard = apps.get_model('content', 'ContentCard')
    if ContentSection.objects.exists():
        return

    CIJProduct = apps.get_model('content', 'CIJProduct')
    TTOProduct = apps.get_model('content', 'TTOProduct')
    LaserProduct = apps.get_model('content', 'LaserProduct')
    QualityCategoryContent = apps.get_model('content', 'QualityCategoryContent')
    QualityProduct = apps.get_model('content', 'QualityProduct')
    LabelingCategoryContent = apps.get_model('content', 'LabelingCategoryContent')
    LabelingProduct = apps.get_model('content', 'LabelingProduct')
    GalleryImage = apps.get_model('content', 'GalleryImage')

    def section(page, slug, **kwargs):
        return ContentSection.objects.create(page=page, slug=slug, **kwargs)

    def card(section_obj, **kwargs):
        return ContentCard.objects.create(section=section_obj, **kwargs)

    # --- Маркування ---
    cij_sec = section(
        'marking', 'cij',
        section_label='Напрям 01 — Маркування',
        title='Каплеструйні маркіратори Linx',
        header_style='category', layout='detail', ordering=10,
    )
    for p in CIJProduct.objects.all():
        card(
            cij_sec,
            card_label=p.get_series_display() if hasattr(p, 'get_series_display') else p.series,
            title=p.title, subtitle=p.subtitle, description=p.description,
            image=p.image, model_tags=p.model_numbers, specs=p.specs,
            slug=f'cij-{p.series}', ordering=p.ordering, is_active=p.is_active,
        )

    tto_sec = section(
        'marking', 'tto',
        section_label='Напрям 01 — Маркування',
        title='Термотрансферні маркіратори Linx',
        header_style='category', layout='detail', ordering=20,
    )
    for p in TTOProduct.objects.all():
        card(
            tto_sec,
            card_label=f'Linx {p.model_series}',
            title=p.title, subtitle=p.subtitle, description=p.description,
            image=p.image, variants=p.variants, print_widths=p.print_widths,
            specs=p.specs, slug=f'tto-{p.model_series.lower()}',
            ordering=p.ordering, is_active=p.is_active,
        )

    laser_sec = section(
        'marking', 'lasers',
        section_label='Напрям 01 — Маркування',
        title='Лазерні маркіратори',
        header_style='category', layout='detail', ordering=30,
    )
    for p in LaserProduct.objects.all():
        card(
            laser_sec,
            card_label=p.get_laser_type_display() if hasattr(p, 'get_laser_type_display') else p.laser_type,
            title=p.title, subtitle=p.subtitle, description=p.description,
            image=p.image, applications=p.applications,
            wavelength=p.wavelength, power_range=p.power_range,
            marking_speed=p.marking_speed, laser_type=p.laser_type,
            brochure=p.brochure, slug=f'{p.laser_type}-laser',
            ordering=p.ordering, is_active=p.is_active,
        )

    # --- КЯ ---
    layout_map = {
        'filling': 'filling',
        'xray': 'gallery',
    }
    order_map = {'filling': 10, 'metal_detector': 20, 'xray': 30, 'checkweigher': 40}
    for cat in QualityCategoryContent.objects.all():
        sec = section(
            'quality', cat.category,
            section_label=cat.section_number,
            section_number=cat.section_number,
            title=cat.section_title,
            body_primary=cat.body_primary,
            body_secondary=cat.body_secondary,
            features_label=cat.features_label,
            features=cat.features,
            header_style='numbered',
            layout=layout_map.get(cat.category, 'grid'),
            ordering=order_map.get(cat.category, cat.ordering),
        )
        if cat.category == 'xray':
            GalleryImage.objects.filter(gallery='xray_foodman').update(section=sec)

    for p in QualityProduct.objects.all():
        sec = ContentSection.objects.filter(page='quality', slug=p.category).first()
        if not sec:
            continue
        card(
            sec,
            title=p.title, slug=p.slug, subtitle=p.subtitle,
            description=p.description, image=p.image, features=p.features,
            ordering=p.ordering, is_active=p.is_active,
        )

    # --- Етикетування ---
    label_order = {'alstep': 10, 'alritma': 20, 'print_apply': 30, 'labelling': 40}
    for cat in LabelingCategoryContent.objects.all():
        section(
            'labeling', cat.category,
            section_number=cat.section_number,
            title=cat.section_title,
            body_primary=cat.body_primary,
            body_secondary=cat.body_secondary,
            features_label=cat.features_label,
            features=cat.features,
            header_style='numbered', layout='grid',
            ordering=label_order.get(cat.category, cat.ordering),
        )

    for p in LabelingProduct.objects.all():
        sec = ContentSection.objects.filter(page='labeling', slug=p.category).first()
        if not sec:
            continue
        card(
            sec,
            title=p.title, subtitle=p.subtitle, description=p.description,
            image=p.image, features=p.features,
            ordering=p.ordering, is_active=p.is_active,
        )
