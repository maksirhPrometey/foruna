from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_nav(context, url_name):
    request = context.get('request')
    if not request:
        return ''
    return 'is-active' if request.resolver_match and request.resolver_match.url_name == url_name else ''


def _ideal_cols(count: int, max_cols: int = 3) -> int:
    """Return the largest divisor of count that is <= max_cols (no orphan cards)."""
    n = max(1, count)
    if n <= max_cols:
        return n
    for c in range(max_cols, 1, -1):
        if n % c == 0:
            return c
    return max_cols


@register.filter(name='ideal_cols')
def ideal_cols_filter(count, max_cols: int = 3) -> int:
    """{{ items|length|ideal_cols:3 }} → integer cols count."""
    try:
        return _ideal_cols(int(count), int(max_cols))
    except (TypeError, ValueError):
        return int(max_cols)
