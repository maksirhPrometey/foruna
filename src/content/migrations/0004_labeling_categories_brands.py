from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_siteconfig_address_fields'),
    ]

    operations = [
        # 1. Оновити CATEGORY_CHOICES у LabelingProduct
        migrations.AlterField(
            model_name='labelingproduct',
            name='category',
            field=models.CharField(
                verbose_name='Категорія',
                max_length=20,
                choices=[
                    ('alstep', 'Аплікатори ALstep'),
                    ('alritma', 'Аплікатори ALritma'),
                    ('print_apply', 'Машини Print&Apply ALcode'),
                    ('labelling', 'Системи етикетування'),
                    ('applicator', 'Аплікатор (заг.)'),
                    ('thermal', 'Термотрансферний принтер'),
                    ('other', 'Інше'),
                ],
                default='other',
            ),
        ),

        # 2. LabelingCategoryContent
        migrations.CreateModel(
            name='LabelingCategoryContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(
                    choices=[
                        ('alstep', 'Аплікатори ALstep'),
                        ('alritma', 'Аплікатори ALritma'),
                        ('print_apply', 'Машини Print&Apply ALcode'),
                        ('labelling', 'Системи етикетування'),
                    ],
                    max_length=20,
                    unique=True,
                    verbose_name='Категорія',
                )),
                ('section_number', models.CharField(blank=True, help_text='Наприклад: 01', max_length=10, verbose_name='Номер секції')),
                ('section_title', models.CharField(max_length=160, verbose_name='Заголовок секції')),
                ('body_primary', models.TextField(verbose_name='Основний текст')),
                ('body_secondary', models.TextField(blank=True, verbose_name='Додатковий текст')),
                ('features_label', models.CharField(blank=True, max_length=160, verbose_name='Заголовок переваг')),
                ('features', models.TextField(blank=True, verbose_name='Переваги (кожна з нового рядка)')),
                ('ordering', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Секція категорії Етикетування',
                'verbose_name_plural': 'Секції категорій Етикетування',
                'ordering': ['ordering'],
            },
        ),

        # 3. Brand
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Назва бренду')),
                ('country', models.CharField(blank=True, max_length=100, verbose_name='Країна')),
                ('founded', models.CharField(blank=True, help_text='Наприклад: 1987', max_length=20, verbose_name='Рік заснування')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='brands/', verbose_name='Логотип')),
                ('description', models.TextField(verbose_name='Опис компанії')),
                ('portfolio', models.TextField(blank=True, verbose_name='Портфоліо / продукти (кожен рядок — окремий пункт)')),
                ('website', models.URLField(blank=True, verbose_name='Вебсайт')),
                ('ordering', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активний')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренди',
                'ordering': ['ordering'],
            },
        ),

        # 4. BrandsPage singleton
        migrations.CreateModel(
            name='BrandsPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_title', models.CharField(blank=True, default='Наші партнери та бренди', max_length=200, verbose_name='Hero — заголовок')),
                ('hero_subtitle', models.TextField(blank=True, default='ФортунаПринт співпрацює з провідними виробниками промислового обладнання зі всього світу — Великобританія, Італія, Китай.', verbose_name='Hero — підзаголовок')),
                ('page_title', models.CharField(blank=True, default='Бренди партнерів | ФортунаПринт', max_length=160, verbose_name='SEO — title')),
                ('meta_description', models.CharField(blank=True, default='Бренди ФортунаПринт: LINX, ALTECH, Easyweigh FOODMAN, T-LINE Technology.', max_length=300, verbose_name='SEO — meta description')),
            ],
            options={
                'verbose_name': 'Сторінка «Бренди»',
                'abstract': False,
            },
        ),
    ]
