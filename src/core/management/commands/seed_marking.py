"""
Заповнення CIJProduct і TTOProduct даними та зображеннями (LINX).

Запуск:
    python manage.py seed_marking
    python manage.py seed_marking --force
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


CIJ_DATA = [
    {
        'series': '89xx',
        'model_numbers': 'Linx 8900, Linx 8920, Linx 8940',
        'title': 'Каплеструйні маркіратори Linx серії 89хх',
        'subtitle': 'Надійні CIJ-маркіратори для харчової, фармацевтичної та промислової галузей',
        'description': (
            'Серія Linx 89хх — провідні каплеструйні маркіратори для нанесення дат, '
            'серійних номерів, штрих-кодів і QR-кодів безпосередньо на рухомому конвеєрі. '
            'Три моделі серії (8900, 8920, 8940) відрізняються висотою друку та '
            'кількістю рядків: від базового однорядкового до трирядкового. '
            'Усі моделі оснащені кольоровим сенсорним дисплеєм і системою '
            'автоматичного очищення голівки. Захист IP55 забезпечує роботу '
            'у вологих і запилених виробничих середовищах.'
        ),
        'specs': (
            'Лінії друку: 1 (8900), 2 (8920), 3 (8940)\n'
            'Висота символу: до 12 мм\n'
            'Швидкість: до 6 м/с\n'
            'Роздільна здатність: до 5×7 крапок\n'
            'Захист: IP55\n'
            'Управління: кольоровий сенсорний дисплей\n'
            'Автоматичне очищення голівки\n'
            'Живлення: 100–240 В, 50/60 Гц'
        ),
        'image': 'marking/cij/linx_8900.jpg',
        'ordering': 1,
    },
    {
        'series': '99xx',
        'model_numbers': 'Linx 9900 Series',
        'title': 'Каплеструйний маркіратор Linx серії 99хх',
        'subtitle': 'Нова флагманська серія CIJ з розширеним набором функцій та захистом IP66',
        'description': (
            'Серія Linx 99хх — новітні каплеструйні маркіратори для сучасних '
            'виробничих ліній. Удосконалена архітектура гідравлічної системи '
            'зменшує час на обслуговування до 35%. Захист IP66 дозволяє '
            'використовувати обладнання у найбільш жорстких умовах виробництва. '
            'Великий кольоровий сенсорний екран із інтуїтивним інтерфейсом '
            'спрощує налаштування і роботу. Підтримка Wi-Fi та Ethernet '
            'забезпечує інтеграцію з системами моніторингу лінії.'
        ),
        'specs': (
            'Висота символу: до 12 мм\n'
            'Захист: IP66\n'
            'Підключення: Wi-Fi, Ethernet\n'
            'Зниження часу обслуговування: -35%\n'
            'Управління: великий кольоровий сенсорний дисплей\n'
            'Автоматичне самоочищення\n'
            'Підтримка Remote Monitor (хмарний моніторинг)'
        ),
        'image': 'marking/cij/linx_99xx.jpg',
        'ordering': 2,
    },
]

TTO_DATA = [
    {
        'model_series': 'TT500',
        'variants': 'Linx TT500 RH',
        'title': 'Термотрансферний маркіратор Linx TT500',
        'subtitle': 'Компактний TTO-принтер для маркування гнучкої та жорсткої упаковки',
        'description': (
            'Linx TT500 RH — компактний термотрансферний оверпринтер для '
            'інтеграції у пакувальні машини. Ідеальний вибір для нанесення '
            'дат виробництва, термінів придатності та серійних номерів на '
            'пакети, стретч-плівку, фольгу та картон. '
            'Конструкція дозволяє встановлення у горизонтальне (RH) положення. '
            'Простий обмін рулонів без зупинки машини.'
        ),
        'print_widths': '32 мм',
        'specs': (
            'Ширина друку: 32 мм\n'
            'Положення: горизонтальне (RH)\n'
            'Швидкість: до 600 мм/с\n'
            'Роздільна здатність: 300 dpi\n'
            'Термін служби голівки: >100 км\n'
            'Інтеграція: сигнал синхронізації з машиною'
        ),
        'image': 'marking/tto/linx_tt500.jpg',
        'ordering': 1,
    },
    {
        'model_series': 'TT750',
        'variants': 'Linx TT750-32 RH, Linx TT750-53 RH',
        'title': 'Термотрансферний маркіратор Linx TT750',
        'subtitle': 'Середня серія TTO: два варіанти ширини друку — 32 і 53 мм',
        'description': (
            'Linx TT750 RH — термотрансферний маркіратор середнього класу '
            'з двома варіантами ширини друку: 32 мм (TT750-32 RH) і '
            '53 мм (TT750-53 RH). Призначений для нанесення багаторядкового '
            'тексту, штрих-кодів і 2D-кодів на гнучку і жорстку упаковку. '
            'Підвищена швидкість друку порівняно з TT500 дозволяє працювати '
            'на швидкісних пакувальних лініях.'
        ),
        'print_widths': '32 мм, 53 мм',
        'specs': (
            'Ширина друку: 32 мм або 53 мм\n'
            'Положення: горизонтальне (RH)\n'
            'Швидкість: до 750 мм/с\n'
            'Роздільна здатність: 300 dpi\n'
            'Підтримка штрих-кодів і QR-кодів\n'
            'Термін служби голівки: >100 км'
        ),
        'image': 'marking/tto/linx_tt750.jpg',
        'ordering': 2,
    },
    {
        'model_series': 'TT1000',
        'variants': 'Linx TT1000-53 RH, Linx TT1000-107 RH',
        'title': 'Термотрансферний маркіратор Linx TT1000',
        'subtitle': 'Флагманська TTO-серія: до 107 мм ширини друку для крупноформатних відбитків',
        'description': (
            'Linx TT1000 RH — флагманська серія термотрансферних маркіраторів '
            'для широкоформатного нанесення. Доступний у двох конфігураціях: '
            '53 мм (TT1000-53 RH) для стандартних застосувань і '
            '107 мм (TT1000-107 RH) для великих форматів. '
            'Висока швидкість до 1000 мм/с підходить для найшвидших '
            'виробничих ліній. Розширена підтримка форматів даних: '
            'GS1, DataMatrix, QR-код, PDF417.'
        ),
        'print_widths': '53 мм, 107 мм',
        'specs': (
            'Ширина друку: 53 мм або 107 мм\n'
            'Положення: горизонтальне (RH)\n'
            'Швидкість: до 1000 мм/с\n'
            'Роздільна здатність: 300 dpi\n'
            'Формати: GS1, DataMatrix, QR, PDF417\n'
            'Термін служби голівки: >100 км'
        ),
        'image': 'marking/tto/linx_tt1000.jpg',
        'ordering': 3,
    },
]


class Command(BaseCommand):
    help = 'Заповнення CIJProduct і TTOProduct даними та зображеннями (LINX)'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Перезаписати існуючі записи')

    def handle(self, *args, **options):
        force = options['force']
        from src.content.models_extra import CIJProduct, TTOProduct

        self.stdout.write(self.style.MIGRATE_HEADING('=== seed_marking: LINX CIJ + TTO ==='))
        try:
            with transaction.atomic():
                self._seed(CIJProduct, CIJ_DATA, 'series', force, 'CIJ')
                self._seed(TTOProduct, TTO_DATA, 'model_series', force, 'TTO')
        except Exception as exc:
            raise CommandError(f'Помилка: {exc}') from exc
        self.stdout.write(self.style.SUCCESS('\n✓ seed_marking завершено успішно.'))

    def _seed(self, model, data_list, key_field, force, label):
        self.stdout.write(f'\n[{label}] Заповнення...')
        for data in data_list:
            key_val = data[key_field]
            image_path = data.pop('image')

            defaults = {k: v for k, v in data.items() if k != key_field}
            if force:
                obj, created = model.objects.update_or_create(
                    **{key_field: key_val}, defaults=defaults,
                )
            else:
                obj, created = model.objects.get_or_create(
                    **{key_field: key_val}, defaults=defaults,
                )

            if created or force or not obj.image:
                obj.image = image_path
                obj.save(update_fields=['image'])

            status = 'створено' if created else ('оновлено' if force else 'вже існує')
            self.stdout.write(f'  [{key_val}] {obj.title[:50]} — {status} | {image_path}')
            data['image'] = image_path
