from django.test import TestCase

from src.content.models import SiteConfig, StatItem, HomePage, LabelingProduct, LabelingPage


class SiteConfigSingletonTest(TestCase):

    def test_load_creates_with_defaults(self):
        site = SiteConfig.load()
        self.assertEqual(site.pk, 1)
        self.assertTrue(site.company_name)
        self.assertTrue(site.phone_1)
        self.assertTrue(site.email)
        self.assertTrue(site.street_address)
        self.assertTrue(site.city)
        self.assertTrue(site.postal_code)

    def test_load_is_idempotent(self):
        s1 = SiteConfig.load()
        s2 = SiteConfig.load()
        self.assertEqual(s1.pk, s2.pk)
        self.assertEqual(SiteConfig.objects.count(), 1)

    def test_save_keeps_pk1(self):
        site = SiteConfig.load()
        site.company_name = 'Тест'
        site.save()
        self.assertEqual(SiteConfig.objects.count(), 1)
        self.assertEqual(SiteConfig.objects.get().company_name, 'Тест')

    def test_address_fields_populated(self):
        site = SiteConfig.load()
        self.assertNotEqual(site.street_address, '')
        self.assertNotEqual(site.city, '')
        self.assertNotEqual(site.postal_code, '')


class StatItemTest(TestCase):

    def test_str(self):
        item = StatItem.objects.create(value='100+', label='Клієнтів', ordering=0)
        self.assertIn('100+', str(item))

    def test_ordering(self):
        StatItem.objects.create(value='A', label='A', ordering=2)
        StatItem.objects.create(value='B', label='B', ordering=1)
        items = list(StatItem.objects.all())
        self.assertEqual(items[0].ordering, 1)
        self.assertEqual(items[1].ordering, 2)


class HomePageM2MTest(TestCase):

    def test_stats_m2m(self):
        page = HomePage.load()
        stat = StatItem.objects.create(value='5', label='Років', ordering=0)
        page.stats.add(stat)
        self.assertIn(stat, page.stats.all())


class LabelingPageM2MTest(TestCase):

    def test_products_m2m(self):
        page = LabelingPage.load()
        product = LabelingProduct.objects.create(
            title='Аплікатор',
            category='applicator',
        )
        page.products.add(product)
        self.assertIn(product, page.products.all())
