from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy


class IndexPageTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='A', email='a@a.com', password='123')

    def test_status_code(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_reverse_lazy_status_code(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertEqual(response.status_code, 200)

    def test_template_use(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertTemplateUsed(response, 'pages/index.html')
