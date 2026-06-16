from src.content.models import SiteConfig


def site_config(request):
    return {'site': SiteConfig.load()}
