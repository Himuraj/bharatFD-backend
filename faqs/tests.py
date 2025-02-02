from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import FAQ

class FAQTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.faq = FAQ.objects.create(
            question='Test Question?',
            answer='Test Answer',
            question_hi='प्रश्न',
            answer_hi='उत्तर'
        )

    def test_get_faqs_english(self):
        url = reverse('faq-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], 'Test Question?')

    def test_get_faqs_hindi(self):
        url = reverse('faq-list')
        response = self.client.get(f'{url}?lang=hi')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], 'प्रश्न')

    def test_search_faqs(self):
        url = reverse('faq-list')
        response = self.client.get(f'{url}?search=Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)