from django.db import models
from django.utils.text import slugify

from src.content.models_gallery import GALLERY_RELATION


# ---------------------------------------------------------------------------
# Global singleton
# ---------------------------------------------------------------------------

class SiteConfig(models.Model):
    """Глобальні контактні дані, що використовуються на всіх сторінках."""
    company_name = models.CharField('Назва компанії', max_length=120, default='ФортунаПринт')
    tagline = models.CharField('Слоган', max_length=200, blank=True)
    phone_1 = models.CharField('Телефон 1', max_length=30, blank=True)
    phone_2 = models.CharField('Телефон 2', max_length=30, blank=True)
    email = models.EmailField('Email', blank=True)
    address = models.TextField('Адреса (повна)', blank=True)
    street_address = models.CharField('Вулиця, будинок', max_length=200, blank=True)
    city = models.CharField('Місто', max_length=100, blank=True)
    postal_code = models.CharField('Поштовий індекс', max_length=20, blank=True)
    website = models.URLField('Сайт', blank=True)

    class Meta:
        verbose_name = 'Налаштування сайту'

    def __str__(self) -> str:
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> 'SiteConfig':
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                'company_name': 'ФортунаПринт',
                'tagline': 'Системи контролю якості · Маркування · Етикетування',
                'phone_1': '+38 050 334 9262',
                'phone_2': '+38 066 424 1553',
                'email': 'info@fortprint.com.ua',
                'address': '02140, Київ, Вишняківська 13а/49',
                'street_address': 'Вишняківська 13а/49',
                'city': 'Київ',
                'postal_code': '02140',
                'website': 'https://www.fortprint.com.ua',
            },
        )
        return obj


# ---------------------------------------------------------------------------
# Shared content blocks
# ---------------------------------------------------------------------------

class StatItem(models.Model):
    """Один статистичний показник для блоку «цифри» на головній сторінці."""
    value = models.CharField('Значення', max_length=30, help_text='Наприклад: 3, HACCP, 24/7')
    label = models.CharField('Підпис', max_length=100)
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Статистичний показник'
        verbose_name_plural = 'Статистичні показники'

    def __str__(self) -> str:
        return f'{self.value} — {self.label}'


class LabelingProduct(models.Model):
    """Обладнання для сторінки «Етикетування» (ALTECH та ін.)."""
    CATEGORY_CHOICES = [
        ('alstep', 'Аплікатори ALstep'),
        ('alritma', 'Аплікатори ALritma'),
        ('print_apply', 'Машини Print&Apply ALcode'),
        ('labelling', 'Системи етикетування'),
        ('applicator', 'Аплікатор (заг.)'),
        ('thermal', 'Термотрансферний принтер'),
        ('other', 'Інше'),
    ]
    category = models.CharField('Категорія', max_length=20, choices=CATEGORY_CHOICES, default='other')
    title = models.CharField('Назва', max_length=160)
    subtitle = models.CharField('Підзаголовок', max_length=255, blank=True)
    description = models.TextField('Опис', blank=True)
    image = models.ImageField('Зображення', upload_to='labeling/', blank=True, null=True)
    features = models.TextField('Характеристики (кожна з нового рядка)', blank=True)
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)
    gallery_images = GALLERY_RELATION

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Обладнання для етикетування'
        verbose_name_plural = 'Обладнання для етикетування'

    def __str__(self) -> str:
        return self.title

    def get_features_list(self) -> list[str]:
        return [line.strip() for line in self.features.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# Quality control category section content
# ---------------------------------------------------------------------------

class QualityCategoryContent(models.Model):
    """Текстовий блок для кожної категорії на сторінці «Контроль якості»."""
    CATEGORY_CHOICES = [
        ('metal_detector', 'Металодетектори'),
        ('xray', 'Рентгенівські інспектори'),
        ('checkweigher', 'Чеквейери'),
        ('filling', 'Системи контролю розливу'),
    ]
    category = models.CharField('Категорія', max_length=20, choices=CATEGORY_CHOICES, unique=True)
    section_number = models.CharField('Номер секції', max_length=10, blank=True, help_text='Наприклад: 01')
    section_title = models.CharField('Заголовок секції', max_length=160)
    body_primary = models.TextField('Основний текст')
    body_secondary = models.TextField('Додатковий текст', blank=True)
    features_label = models.CharField('Заголовок переваг', max_length=160, blank=True,
                                      help_text='Наприклад: «Переваги металодетекторів»')
    features = models.TextField('Переваги (кожна з нового рядка)', blank=True)
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Секція категорії КЯ'
        verbose_name_plural = 'Секції категорій КЯ'

    def __str__(self) -> str:
        return self.get_category_display()

    def get_features_list(self) -> list[str]:
        return [line.strip() for line in self.features.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# Labeling category section content
# ---------------------------------------------------------------------------

class LabelingCategoryContent(models.Model):
    """Текстовий блок для кожної категорії на сторінці «Етикетування»."""
    CATEGORY_CHOICES = [
        ('alstep', 'Аплікатори ALstep'),
        ('alritma', 'Аплікатори ALritma'),
        ('print_apply', 'Машини Print&Apply ALcode'),
        ('labelling', 'Системи етикетування'),
    ]
    category = models.CharField('Категорія', max_length=20, choices=CATEGORY_CHOICES, unique=True)
    section_number = models.CharField('Номер секції', max_length=10, blank=True, help_text='Наприклад: 01')
    section_title = models.CharField('Заголовок секції', max_length=160)
    body_primary = models.TextField('Основний текст')
    body_secondary = models.TextField('Додатковий текст', blank=True)
    features_label = models.CharField('Заголовок переваг', max_length=160, blank=True)
    features = models.TextField('Переваги (кожна з нового рядка)', blank=True)
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Секція категорії Етикетування'
        verbose_name_plural = 'Секції категорій Етикетування'

    def __str__(self) -> str:
        return self.get_category_display()

    def get_features_list(self) -> list[str]:
        return [line.strip() for line in self.features.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# Page singleton mixin
# ---------------------------------------------------------------------------

class _PageSingleton(models.Model):
    """Базовий клас для унікальних сторінок (pk=1, load())."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults=cls._defaults())
        return obj

    @classmethod
    def _defaults(cls) -> dict:
        return {}


# ---------------------------------------------------------------------------
# Page models
# ---------------------------------------------------------------------------

class HomePage(_PageSingleton):
    """Контент головної сторінки."""
    # Hero
    hero_title = models.CharField('Hero — заголовок', max_length=200, blank=True,
                                  default='Промислове обладнання для маркування, контролю та етикетування')
    hero_subtitle = models.TextField('Hero — підзаголовок', blank=True,
                                     default='Постачання та впровадження обладнання для виробничих ліній — від лазерного маркування до систем контролю якості HACCP.')
    # Напрями
    directions_section_title = models.CharField('Напрями — заголовок розділу', max_length=200, blank=True,
                                                default='Повний спектр промислових рішень від єдиного експерта')
    # Про компанію
    about_title = models.TextField('Про нас — заголовок', blank=True,
                                   default='ТОВ «ФортунаПринт» — команда експертів у сфері промислового маркування та етикетування з понад 25-річним досвідом роботи.')
    about_body_1 = models.TextField('Про нас — абзац 1', blank=True,
                                    default='Ми пропонуємо комплексні рішення для бізнесу: від підбору та постачання сучасного маркувального й етикетувального обладнання до впровадження систем контролю якості на виробництві. Наші технології та рішення успішно використовуються підприємствами різних галузей промисловості по всій Україні.')
    about_body_2 = models.TextField('Про нас — абзац 2', blank=True,
                                    default='Основою успіху компанії є наші фахівці. Багаторічний досвід, десятки реалізованих проєктів і глибока технічна експертиза дозволяють нам ефективно вирішувати навіть найскладніші виробничі завдання.')
    about_body_3 = models.TextField('Про нас — абзац 3', blank=True,
                                    default='Ми не обмежуємося постачанням обладнання. Наша мета — допомагати клієнтам оптимізувати виробничі процеси, підвищувати якість продукції, збільшувати продуктивність та скорочувати операційні витрати.')
    about_body_4 = models.TextField('Про нас — абзац 4', blank=True,
                                    default='Обираючи ТОВ «ФортунаПринт», ви отримуєте надійного партнера, який розуміє специфіку вашої галузі та пропонує ефективні, перевірені практикою рішення для розвитку вашого бізнесу.')
    # Stats
    stats = models.ManyToManyField(StatItem, verbose_name='Статистика', blank=True)
    # CTA
    cta_title = models.CharField('CTA — заголовок', max_length=200, blank=True,
                                 default='Підберемо обладнання під ваші задачі')
    cta_body = models.TextField('CTA — текст', blank=True,
                                default='Залиште заявку — наш спеціаліст зв\u2019яжеться з вами та запропонує оптимальне рішення.')
    # SEO
    page_title = models.CharField('SEO — title', max_length=160, blank=True,
                                  default='ФортунаПринт — Маркування, Контроль якості, Етикетування')
    meta_description = models.CharField('SEO — meta description', max_length=300, blank=True)

    class Meta:
        verbose_name = 'Головна сторінка'

    def __str__(self) -> str:
        return 'Головна сторінка'

    @classmethod
    def _defaults(cls) -> dict:
        return {}


class MarkingPage(_PageSingleton):
    """Контент сторінки «Маркування»."""
    # Hero
    hero_direction_label = models.CharField('Hero — мітка напряму', max_length=30, blank=True, default='Напрям 01')
    hero_title = models.CharField('Hero — заголовок', max_length=200, blank=True, default='Маркування')
    hero_subtitle = models.TextField('Hero — підзаголовок', blank=True,
                                     default='Повний спектр маркувальних технологій в одних руках — це ваш надійний партнер у автоматизації виробничих процесів та ідентифікації товарів. Ми забезпечуємо бізнес усім необхідним: від підбору обладнання під ключ до постачання оригінальних витратних матеріалів і сервісу.')
    # Intro
    intro_title = models.CharField('Intro — заголовок', max_length=200, blank=True,
                                   default='Чому лазерне маркування?')
    intro_body_1 = models.TextField('Intro — абзац 1', blank=True,
                                    default='Лазерне маркування є незамінним на сучасному виробництві — воно забезпечує стійке, нестираємо маркування без використання хімікатів та витратних матеріалів.')
    intro_body_2 = models.TextField('Intro — абзац 2', blank=True,
                                    default='Ми постачаємо китайські лазерні маркіратори трьох типів: ультрафіолетові (УФ), CO₂ та файбер (волоконні). Кожен тип оптимізовано для конкретних матеріалів та задач.')
    # CTA
    cta_title = models.CharField('CTA — заголовок', max_length=200, blank=True,
                                 default='Підберемо лазерний маркіратор для вашого виробництва')
    cta_body = models.TextField('CTA — текст', blank=True,
                                default='Вкажіть матеріал, швидкість лінії та тип маркування — ми запропонуємо оптимальне рішення.')
    # SEO
    page_title = models.CharField('SEO — title', max_length=160, blank=True,
                                  default='Маркування — Лазерні маркіратори | ФортунаПринт')
    meta_description = models.CharField('SEO — meta description', max_length=300, blank=True,
                                        default='Лазерні маркіратори для промислового застосування: УФ, CO₂, файбер лазери.')

    class Meta:
        verbose_name = 'Сторінка «Маркування»'

    def __str__(self) -> str:
        return 'Маркування'


class QualityControlPage(_PageSingleton):
    """Контент сторінки «Контроль якості»."""
    # Hero
    hero_direction_label = models.CharField('Hero — мітка напряму', max_length=30, blank=True, default='Напрям 02')
    hero_title = models.CharField('Hero — заголовок', max_length=200, blank=True,
                                  default='Системи контролю якості')
    hero_subtitle = models.TextField('Hero — підзаголовок', blank=True,
                                     default='Комплексні рішення для інспекції продукції на виробничій лінії. Металодетектори, рентгенівські інспектори, чеквейери та системи контролю розливу — все для виконання вимог HACCP.')
    # HACCP intro
    haccp_intro_title = models.CharField('HACCP — заголовок', max_length=200, blank=True,
                                         default='Контроль якості для виконання HACCP')
    haccp_body_1 = models.TextField('HACCP — абзац 1', blank=True,
                                    default='Кожен виробник продукції стикається з необхідністю встановлення інспекційного обладнання як ККТ (Критичної Контрольної Точки) для виконання плану HACCP.')
    haccp_body_2 = models.TextField('HACCP — абзац 2', blank=True,
                                    default='Системи інспекції виробництва T-LINE Technology Co., Ltd забезпечують контроль рівня наливу, укупорки, етикетування, маркування та цілісності тари. При виявленні відхилень — автоматичне відбракування пневматичним пушером.')
    # CTA
    cta_title = models.CharField('CTA — заголовок', max_length=200, blank=True,
                                 default='Підберемо систему контролю якості під ваш HACCP-план')
    cta_body = models.TextField('CTA — текст', blank=True,
                                default='Опишіть вашу виробничу лінію — ми запропонуємо відповідне рішення.')
    # Додаткові блоки розділу «Контроль розливу»
    filling_extra_1_title = models.CharField(
        'Розлив — блок 1 заголовок', max_length=200, blank=True,
        default='Рентген інспектор рівня наливу',
    )
    filling_extra_1_body = models.TextField(
        'Розлив — блок 1 текст', blank=True,
        default=(
            'Інспектор дозволяє визначити коректність рівня наповнення та закупорювання '
            'в скляних-, ПЕТ пляшках та алюмінієвих та жерстяних банках. Система дозволяє '
            'безконтактно визначити недолив та/або перелив, у тому числі і піниться продукту. '
            'Як опція для даної системи пропонуються:'
        ),
    )
    filling_extra_1_features = models.TextField(
        'Розлив — блок 1 пункти (кожен з нового рядка)', blank=True,
        default='функція контролю наявності кришки\nфункція контролю наявності етикетки\nфункція FMS',
    )
    filling_extra_2_title = models.CharField(
        'Розлив — блок 2 заголовок', max_length=200, blank=True,
        default='Інспектор групової упаковки',
    )
    filling_extra_2_body = models.TextField(
        'Розлив — блок 2 текст', blank=True,
        default=(
            'Система використовує зв\'язок з рентгенівським випромінювачем і детектором, '
            'який на основі безконтактної технології виявлення забезпечує перевірку групової '
            'упаковки з продуктами розливу і дозволяє відбракувати групові упаковки, '
            'що не пройшли кваліфікацію.'
        ),
    )
    # SEO
    page_title = models.CharField('SEO — title', max_length=160, blank=True,
                                  default='Системи контролю якості | ФортунаПринт')
    meta_description = models.CharField('SEO — meta description', max_length=300, blank=True,
                                        default='Обладнання для контролю якості: металодетектори, рентгенівські інспектори, чеквейери, системи контролю розливу. HACCP.')

    class Meta:
        verbose_name = 'Сторінка «Контроль якості»'

    def __str__(self) -> str:
        return 'Контроль якості'

    def get_filling_extra_1_features_list(self) -> list[str]:
        return [line.strip() for line in self.filling_extra_1_features.splitlines() if line.strip()]


class LabelingPage(_PageSingleton):
    """Контент сторінки «Етикетування»."""
    # Hero
    hero_direction_label = models.CharField('Hero — мітка напряму', max_length=30, blank=True, default='Напрям 03')
    hero_title = models.CharField('Hero — заголовок', max_length=200, blank=True, default='Етикетування')
    hero_subtitle = models.TextField('Hero — підзаголовок', blank=True,
                                     default='Автоматичні та напівавтоматичні системи нанесення етикеток для виробничих ліній. Рішення для будь-яких типів тари та форм упаковки.')
    # CTA
    cta_title = models.CharField('CTA — заголовок', max_length=200, blank=True,
                                 default='Залиште заявку на підбір обладнання для етикетування')
    cta_body = models.TextField('CTA — текст', blank=True,
                                default='Ми зв\u2019яжемось з вами та надамо повну інформацію.')
    # Products
    products = models.ManyToManyField(LabelingProduct, verbose_name='Обладнання', blank=True)
    # SEO
    page_title = models.CharField('SEO — title', max_length=160, blank=True,
                                  default='Етикетування — Обладнання для нанесення етикеток | ФортунаПринт')
    meta_description = models.CharField('SEO — meta description', max_length=300, blank=True,
                                        default='Промислове обладнання для нанесення етикеток. Автоматичні та напівавтоматичні аплікатори для виробничих ліній.')

    class Meta:
        verbose_name = 'Сторінка «Етикетування»'

    def __str__(self) -> str:
        return 'Етикетування'


class ContactsPage(_PageSingleton):
    """Контент сторінки «Контакти»."""
    intro_text = models.TextField('Вступний текст', blank=True,
                                  default='Ми раді відповісти на ваші запитання та допомогти підібрати обладнання для вашого виробництва.')
    page_title = models.CharField('SEO — title', max_length=160, blank=True,
                                  default='Контакти | ФортунаПринт')
    meta_description = models.CharField('SEO — meta description', max_length=300, blank=True,
                                        default='Зв\u2019яжіться з ФортунаПринт: Київ, Вишняківська 13а/49.')

    class Meta:
        verbose_name = 'Сторінка «Контакти»'

    def __str__(self) -> str:
        return 'Контакти'


# ---------------------------------------------------------------------------
# Product catalogs (existing)
# ---------------------------------------------------------------------------

class LaserProduct(models.Model):
    LASER_TYPES = [
        ('uv', 'УФ лазер'),
        ('co2', 'CO₂ лазер'),
        ('fiber', 'Файбер лазер'),
    ]
    laser_type = models.CharField('Тип лазера', max_length=10, choices=LASER_TYPES, unique=True)
    title = models.CharField('Назва', max_length=160)
    subtitle = models.CharField('Підзаголовок', max_length=255, blank=True)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='lasers/', blank=True, null=True)
    brochure = models.FileField(
        'PDF-брошура', upload_to='brochures/lasers/', blank=True, null=True,
        help_text='Якщо порожньо — використовується файл з /static/brochures/lasers/',
    )
    applications = models.TextField('Сфери застосування (кожна з нового рядка)', blank=True)
    power_range = models.CharField('Діапазон потужності', max_length=80, blank=True)
    wavelength = models.CharField('Довжина хвилі', max_length=80, blank=True)
    marking_speed = models.CharField('Швидкість маркування', max_length=80, blank=True)
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)
    meta_description = models.CharField('Meta description', max_length=300, blank=True)
    is_active = models.BooleanField('Активний', default=True)
    gallery_images = GALLERY_RELATION

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Лазерний маркіратор'
        verbose_name_plural = 'Лазерні маркіратори'

    def __str__(self) -> str:
        return f'{self.get_laser_type_display()} — {self.title}'

    def get_applications_list(self) -> list[str]:
        return [line.strip() for line in self.applications.splitlines() if line.strip()]


class QualityProduct(models.Model):
    CATEGORY_CHOICES = [
        ('metal_detector', 'Металодетектор'),
        ('xray', 'Рентгенівський інспектор'),
        ('checkweigher', 'Чеквейер'),
        ('filling', 'Система контролю розливу'),
    ]
    category = models.CharField('Категорія', max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField('Назва', max_length=160)
    slug = models.SlugField('Slug', unique=True, blank=True, max_length=200)
    subtitle = models.CharField('Підзаголовок', max_length=255, blank=True)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='quality/', blank=True, null=True)
    features = models.TextField('Переваги (кожна з нового рядка)', blank=True)
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)
    gallery_images = GALLERY_RELATION

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Обладнання контролю якості'
        verbose_name_plural = 'Обладнання контролю якості'

    def __str__(self) -> str:
        return f'{self.get_category_display()} — {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_features_list(self) -> list[str]:
        return [line.strip() for line in self.features.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# Brands
# ---------------------------------------------------------------------------

class Brand(models.Model):
    """Бренд / партнер компанії."""
    name = models.CharField('Назва бренду', max_length=120)
    country = models.CharField('Країна', max_length=100, blank=True)
    founded = models.CharField('Рік заснування', max_length=20, blank=True,
                               help_text='Наприклад: 1987')
    logo = models.ImageField('Логотип', upload_to='brands/', blank=True, null=True)
    description = models.TextField('Опис компанії')
    portfolio = models.TextField('Портфоліо / продукти (кожен рядок — окремий пункт)', blank=True)
    website = models.URLField('Вебсайт', blank=True)
    ordering = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)
    gallery_images = GALLERY_RELATION

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'

    def __str__(self) -> str:
        return self.name

    def get_portfolio_list(self) -> list[str]:
        return [line.strip() for line in self.portfolio.splitlines() if line.strip()]


from src.content.models_extra import CIJProduct, TTOProduct, GalleryImage  # noqa: E402
from src.content.models_gallery import ProductGalleryImage  # noqa: E402
from src.content.models_sections import ContentSection, ContentCard  # noqa: E402


class BrandsPage(_PageSingleton):
    """Контент сторінки «Бренди»."""
    hero_title = models.CharField('Hero — заголовок', max_length=200, blank=True,
                                  default='Наші партнери та бренди')
    hero_subtitle = models.TextField('Hero — підзаголовок', blank=True,
                                     default='ФортунаПринт співпрацює з провідними виробниками промислового обладнання зі всього світу — Великобританія, Італія, Китай.')
    page_title = models.CharField('SEO — title', max_length=160, blank=True,
                                  default='Бренди партнерів | ФортунаПринт')
    meta_description = models.CharField('SEO — meta description', max_length=300, blank=True,
                                        default='Бренди ФортунаПринт: LINX, ALTECH, Easyweigh FOODMAN, T-LINE Technology.')

    class Meta:
        verbose_name = 'Сторінка «Бренди»'

    def __str__(self) -> str:
        return 'Бренди'
