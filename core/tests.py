from django.test import TestCase, Client
from django.urls import reverse
from core.models import SiteSettings, Testimonial, Page
from products.models import Product, ProductCategory, Brand
from services.models import Service, ServiceCategory, CCTVPricing


class PlatformCoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.settings = SiteSettings.get_settings()
        self.pricing = CCTVPricing.get_pricing()

    def test_homepage_status(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_about_status(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)

    def test_contact_status(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)

    def test_cctv_calculator_status(self):
        response = self.client.get(reverse('services:cctv_calculator'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_status(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_service_list_status(self):
        response = self.client.get(reverse('services:service_list'))
        self.assertEqual(response.status_code, 200)

    def test_sitemap_xml(self):
        response = self.client.get(reverse('core:sitemap'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response['Content-Type'])

    def test_robots_txt(self):
        response = self.client.get(reverse('core:robots'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response['Content-Type'])
