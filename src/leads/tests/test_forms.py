from django.test import TestCase

from src.leads.forms import LeadForm


class LeadFormTest(TestCase):
    def _valid_data(self, **overrides):
        return {'name': 'Іван Петренко', 'phone': '+380501234567', 'source': 'contact', **overrides}

    def test_valid_form(self):
        form = LeadForm(data=self._valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_name_required(self):
        form = LeadForm(data=self._valid_data(name=''))
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_phone_required(self):
        form = LeadForm(data=self._valid_data(phone=''))
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_message_not_required(self):
        form = LeadForm(data=self._valid_data(message=''))
        self.assertTrue(form.is_valid(), form.errors)

    def test_source_not_required(self):
        form = LeadForm(data=self._valid_data(source=''))
        self.assertTrue(form.is_valid(), form.errors)

    def test_name_max_length(self):
        form = LeadForm(data=self._valid_data(name='A' * 121))
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_phone_max_length(self):
        form = LeadForm(data=self._valid_data(phone='0' * 31))
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
