from django.views.generic import TemplateView

from src.content.models import (
    HomePage,
    MarkingPage,
    QualityControlPage,
    LabelingPage,
    ContactsPage,
    Brand,
    BrandsPage,
    LaserProduct,
)
from src.core.section_context import sections_for_page
from src.leads.forms import LeadForm


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        home = HomePage.load()
        ctx['home'] = home
        ctx['page_title'] = home.page_title
        ctx['meta_description'] = home.meta_description
        ctx['lasers'] = LaserProduct.objects.filter(is_active=True)
        ctx['quality_categories'] = [
            {'key': 'metal_detector', 'label': 'Металодетектори'},
            {'key': 'xray', 'label': 'Рентгенівські інспектори'},
            {'key': 'checkweigher', 'label': 'Чеквейери'},
            {'key': 'filling', 'label': 'Контроль розливу'},
        ]
        ctx['stats'] = home.stats.all()
        ctx['form'] = LeadForm(initial={'source': 'contact'})
        return ctx


class MarkingView(TemplateView):
    template_name = 'pages/marking.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = MarkingPage.load()
        ctx['marking'] = page
        ctx['page_title'] = page.page_title
        ctx['meta_description'] = page.meta_description
        ctx['page_sections'] = sections_for_page('marking')
        ctx['form'] = LeadForm(initial={'source': 'marking'})
        return ctx


class QualityControlView(TemplateView):
    template_name = 'pages/quality_control.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = QualityControlPage.load()
        ctx['qc'] = page
        ctx['page_title'] = page.page_title
        ctx['meta_description'] = page.meta_description
        ctx['page_sections'] = sections_for_page('quality')
        ctx['form'] = LeadForm(initial={'source': 'quality'})
        return ctx


class LabelingView(TemplateView):
    template_name = 'pages/labeling.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = LabelingPage.load()
        ctx['labeling'] = page
        ctx['page_title'] = page.page_title
        ctx['meta_description'] = page.meta_description
        ctx['page_sections'] = sections_for_page('labeling')
        ctx['form'] = LeadForm(initial={'source': 'labeling'})
        return ctx


class ContactsView(TemplateView):
    template_name = 'pages/contacts.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = ContactsPage.load()
        ctx['contacts'] = page
        ctx['page_title'] = page.page_title
        ctx['meta_description'] = page.meta_description
        ctx['form'] = LeadForm(initial={'source': 'contact'})
        return ctx


class BrandsView(TemplateView):
    template_name = 'pages/brands.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = BrandsPage.load()
        ctx['brands_page'] = page
        ctx['page_title'] = page.page_title
        ctx['meta_description'] = page.meta_description
        ctx['brands'] = Brand.objects.filter(is_active=True)
        ctx['form'] = LeadForm(initial={'source': 'contact'})
        return ctx
