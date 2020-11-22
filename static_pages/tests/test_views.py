from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_page_accessible_by_name(self):
        """URL, генерируемый при помощи имени static_pages:about, доступен."""
        response = self.guest_client.get(reverse('static_pages:about'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        """При запросе к staticpages:about
        применяется шаблон staticpages/about.html."""
        response = self.guest_client.get(reverse('static_pages:about'))
        self.assertTemplateUsed(response, 'static_pages/about.html')
