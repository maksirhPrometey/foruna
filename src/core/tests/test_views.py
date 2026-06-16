from django.test import TestCase

from src.content.models import (
    HomePage, MarkingPage, QualityControlPage, LabelingPage, ContactsPage,
)


class PageViewsTest(TestCase):
    """Smoke tests: all pages return 200 and use correct templates."""

    def test_home_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_marking_200(self):
        response = self.client.get('/marking/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/marking.html')

    def test_quality_control_200(self):
        response = self.client.get('/quality-control/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/quality_control.html')

    def test_labeling_200(self):
        response = self.client.get('/labeling/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/labeling.html')

    def test_contacts_200(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/contacts.html')


class PageSingletonTest(TestCase):
    """load() creates singleton with defaults on first call."""

    def test_home_page_load_creates_singleton(self):
        page = HomePage.load()
        self.assertEqual(page.pk, 1)
        self.assertTrue(page.hero_title)

    def test_home_page_second_load_returns_same(self):
        p1 = HomePage.load()
        p2 = HomePage.load()
        self.assertEqual(p1.pk, p2.pk)

    def test_marking_page_load(self):
        page = MarkingPage.load()
        self.assertEqual(page.pk, 1)
        self.assertTrue(page.hero_title)

    def test_quality_control_page_load(self):
        page = QualityControlPage.load()
        self.assertEqual(page.pk, 1)
        self.assertTrue(page.hero_title)

    def test_labeling_page_load(self):
        page = LabelingPage.load()
        self.assertEqual(page.pk, 1)
        self.assertTrue(page.hero_title)

    def test_contacts_page_load(self):
        page = ContactsPage.load()
        self.assertEqual(page.pk, 1)
        self.assertTrue(page.intro_text)

    def test_home_page_save_keeps_pk1(self):
        page = HomePage.load()
        page.hero_title = 'Новий заголовок'
        page.save()
        self.assertEqual(HomePage.objects.count(), 1)
        self.assertEqual(HomePage.objects.get().hero_title, 'Новий заголовок')
