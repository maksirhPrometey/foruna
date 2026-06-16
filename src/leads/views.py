import html
import json
import logging
import threading
import urllib.request
from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.template.response import TemplateResponse
from django.conf import settings

from .forms import LeadForm
from .models import Lead

logger = logging.getLogger(__name__)

_RL_REQUESTS = 5   # max submissions per IP
_RL_WINDOW = 60    # seconds


def _get_client_ip(request) -> str:
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def _is_rate_limited(ip: str) -> bool:
    key = f'lead_rl:{ip}'
    cache.add(key, 0, _RL_WINDOW)
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, _RL_WINDOW)
        count = 1
    return count > _RL_REQUESTS


def _notify_telegram(lead: Lead) -> None:
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        return
    text = (
        f'📩 Нова заявка з сайту FortunaPrint\n'
        f'Ім\'я: {html.escape(lead.name)}\n'
        f'Телефон: {html.escape(lead.phone)}\n'
        f'Джерело: {html.escape(lead.get_source_display())}\n'
    )
    if lead.message:
        text += f'Повідомлення: {html.escape(lead.message)}\n'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = json.dumps({'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        logger.exception('Помилка надсилання Telegram-сповіщення для lead_id=%s', lead.pk)


@require_POST
def lead_submit(request):
    if _is_rate_limited(_get_client_ip(request)):
        return HttpResponse(status=429)

    form = LeadForm(request.POST)
    if form.is_valid() and not request.POST.get('honeypot'):
        lead = Lead.objects.create(
            name=form.cleaned_data['name'],
            phone=form.cleaned_data['phone'],
            message=form.cleaned_data.get('message', ''),
            source=form.cleaned_data.get('source') or 'contact',
        )
        threading.Thread(target=_notify_telegram, args=(lead,), daemon=True).start()
        return TemplateResponse(request, 'partials/lead_success.html', {})
    return TemplateResponse(request, 'partials/lead_form.html', {'form': form})
