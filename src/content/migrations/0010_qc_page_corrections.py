# Generated manually for QC page content corrections

from django.db import migrations


def apply_qc_corrections(apps, schema_editor):
    QualityProduct = apps.get_model('content', 'QualityProduct')
    QualityCategoryContent = apps.get_model('content', 'QualityCategoryContent')

    QualityProduct.objects.filter(
        category='xray',
        title__icontains='рівень наливу',
    ).update(is_active=False)

    QualityCategoryContent.objects.filter(category='filling').update(
        body_secondary='',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_marking_hero_subtitle'),
    ]

    operations = [
        migrations.RunPython(apply_qc_corrections, migrations.RunPython.noop),
    ]
