"""Імпорт динамічного контенту з папки content/."""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from src.core.content_data.importer import import_content


class Command(BaseCommand):
    help = 'Імпорт текстів, зображень і PDF з папки content/ у БД'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir',
            default='content',
            help='Шлях до папки контенту (відносно BASE_DIR або абсолютний)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перезаписати існуючі записи',
        )

    def handle(self, *args, **options):
        raw = options['dir']
        content_dir = Path(raw)
        if not content_dir.is_absolute():
            content_dir = Path(settings.BASE_DIR) / content_dir

        self.stdout.write(self.style.MIGRATE_HEADING(
            f'=== import_content ← {content_dir} ==='))

        try:
            import_content(content_dir, force=options['force'], stdout=self.stdout)
        except FileNotFoundError as exc:
            raise CommandError(str(exc)) from exc
        except Exception as exc:
            raise CommandError(f'Помилка імпорту: {exc}') from exc

        self.stdout.write(self.style.SUCCESS(
            '\n✓ Імпорт завершено. На продакшені також:\n'
            '  python manage.py collectstatic --noinput --clear\n'
            '  touch passenger_wsgi.py   # перезапуск ADM.TOOLS Passenger'))
