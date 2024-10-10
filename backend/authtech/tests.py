# authtech/tests.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Product, Transaction

class ProductVerificationTestCase(APITestCase):
    
    def setUp(self):
        # Create a user to authenticate the API requests
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create sample products for testing
        self.product_genuine = Product.objects.create(name="Genuine Product", code="12345", status="genuine")
        self.product_fake = Product.objects.create(name="Fake Product", code="54321", status="fake")
        self.product_used = Product.objects.create(name="Used Product", code="67890", status="used")

        # URL for the product verification endpoint
        self.url = reverse('verify_product')

    def test_verify_genuine_product(self):
        # Test verifying a genuine product
        data = {'product_code': '12345'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'genuine')

        # Check that a transaction was created
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.product, self.product_genuine)
        self.assertEqual(transaction.status, 'genuine')

    def test_verify_fake_product(self):
        # Test verifying a fake product
        data = {'product_code': '54321'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'fake')

        # Check that a transaction was created
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.product, self.product_fake)
        self.assertEqual(transaction.status, 'fake')

    def test_verify_used_product(self):
        # Test verifying a used product
        data = {'product_code': '67890'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('used', response.data['status'])

        # Check that a transaction was created
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.product, self.product_used)
        self.assertEqual(transaction.status, 'used')

    def test_verify_non_existent_product(self):
        # Test verifying a non-existent product
        data = {'product_code': '99999'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'unknown')

        # Check that a transaction was created even for unknown product
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertIsNone(transaction.product)
        self.assertEqual(transaction.status, 'unknown')

    def test_unauthorized_access(self):
        # Test unauthorized access
        data = {'product_code': '12345'}
        self.client.logout()
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
