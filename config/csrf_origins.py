"""Побудова CSRF_TRUSTED_ORIGINS для production за ALLOWED_HOSTS."""

from __future__ import annotations

from decouple import config


def build_csrf_trusted_origins(allowed_hosts: list[str]) -> list[str]:
    """
    Django 4+ вимагає CSRF_TRUSTED_ORIGINS для HTTPS POST.
    Якщо змінна в .env порожня — будуємо з ALLOWED_HOSTS + домени FortunaPrint.
    """
    configured = config(
        'CSRF_TRUSTED_ORIGINS',
        default='',
        cast=lambda v: [s.strip() for s in v.split(',') if s.strip()],
    )
    if configured:
        return configured

    candidates: list[str] = [
        'https://fortprint.com.ua',
        'https://www.fortprint.com.ua',
    ]

    for host in allowed_hosts:
        host = host.strip()
        if not host or host.startswith('.'):
            continue
        if host in ('localhost', '127.0.0.1', '[::1]'):
            candidates.extend([
                f'http://{host}',
                f'http://{host}:8000',
            ])
            continue
        if host.replace('.', '').isdigit():
            candidates.extend([f'http://{host}', f'https://{host}'])
            continue
        candidates.append(f'https://{host}')
        if not host.startswith('www.'):
            candidates.append(f'https://www.{host}')

    seen: set[str] = set()
    result: list[str] = []
    for origin in candidates:
        if origin not in seen:
            seen.add(origin)
            result.append(origin)
    return result
