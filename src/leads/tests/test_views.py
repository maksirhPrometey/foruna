from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from src.leads.models import Lead


class LeadSubmitViewTest(TestCase):
    URL = '/leads/submit/'

    def _post(self, data=None):
        payload = {'name': 'Тест', 'phone': '+380991234567', 'source': 'contact', 'honeypot': '', **(data or {})}
        return self.client.post(self.URL, payload)

    @patch('src.leads.views._notify_telegram')
    def test_valid_submission_creates_lead(self, mock_notify):
        response = self._post()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/lead_success.html')
        self.assertEqual(Lead.objects.count(), 1)
        lead = Lead.objects.first()
        self.assertEqual(lead.name, 'Тест')
        self.assertEqual(lead.phone, '+380991234567')
        self.assertEqual(lead.source, 'contact')
        mock_notify.assert_called_once_with(lead)

    @patch('src.leads.views._notify_telegram')
    def test_honeypot_blocks_submission(self, mock_notify):
        response = self._post({'honeypot': 'bot-fill'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)
        mock_notify.assert_not_called()

    def test_invalid_form_returns_form_partial(self):
        response = self.client.post(self.URL, {'name': '', 'phone': '', 'honeypot': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/lead_form.html')
        self.assertEqual(Lead.objects.count(), 0)

    def test_get_not_allowed(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 405)

    @patch('src.leads.views._notify_telegram')
    def test_source_saved_from_form(self, mock_notify):
        self._post({'source': 'marking'})
        self.assertEqual(Lead.objects.first().source, 'marking')

    @patch('src.leads.views._notify_telegram')
    def test_missing_source_defaults_to_contact(self, mock_notify):
        self._post({'source': ''})
        self.assertEqual(Lead.objects.first().source, 'contact')
