"""Експорт динамічного контенту у папку content/."""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from src.core.content_data.exporter import export_content


class Command(BaseCommand):
    help = 'Експорт текстів, зображень і PDF у папку content/ (JSON + assets)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir',
            default='content',
            help='Шлях до папки контенту (відносно BASE_DIR або абсолютний)',
        )

    def handle(self, *args, **options):
        raw = options['dir']
        content_dir = Path(raw)
        if not content_dir.is_absolute():
            content_dir = Path(settings.BASE_DIR) / content_dir

        try:
            stats = export_content(content_dir)
        except Exception as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(self.style.MIGRATE_HEADING(
            f'=== export_content → {stats["root"]} ==='))
        self.stdout.write(f'JSON-файлів: {stats["json_files"]}')
        self.stdout.write(f'PDF (static): {stats["static_files"]}')
        self.stdout.write(f'Зображень (media): {stats["media_files"]}')

        if stats['media_missing']:
            self.stdout.write(self.style.WARNING(
                f'\n⚠ Не знайдено локально {len(stats["media_missing"])} зображень '
                f'(шляхи збережено в JSON, додайте файли в assets/media/):'))
            for path in stats['media_missing'][:10]:
                self.stdout.write(f'  - {path}')
            if len(stats['media_missing']) > 10:
                self.stdout.write(f'  ... і ще {len(stats["media_missing"]) - 10}')

        self.stdout.write(self.style.SUCCESS(
            '\n✓ Експорт завершено. Перенесіть папку content/ на сервер і запустіть:\n'
            '  python manage.py import_content --force\n'
            '  python manage.py collectstatic --noinput'))
