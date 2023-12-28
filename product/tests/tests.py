from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from product.models import Product

class ProductListCreateViewTestCase(TestCase):
    """
    Test Cases for list and create customer.
    """
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('product_list')
        self.create_url = reverse('product_create')

    def test_list_customers(self):
        # Create some products for testing
        Product.objects.create(name='Prod 1', price = 1000, stock_quantity=5)
        Product.objects.create(name='Prod 2', price = 500, stock_quantity=2)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check the number of Products returned

    def test_create_customer(self):
        # Create product for testing
        data = {'name': 'Prod 1', 'price': 250, 'stock_quantity':3}

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)  # Check if the product was created
        self.assertEqual(Product.objects.first().name, 'Prod 1')
