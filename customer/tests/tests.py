from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from customer.models import Customer

class CustomerListCreateViewTestCase(TestCase):
    """
    Test Cases for list and create customer.
    """
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('customer_list')
        self.create_url = reverse('customer_create')

    def test_list_customers(self):
        # Create some customers for testing
        Customer.objects.create(name='Ali')
        Customer.objects.create(name='Hassan')

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check the number of customers returned

    def test_create_customer(self):
        # Create some customers for testing
        data = {'name': 'Mohamed Ayman'}

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)  # Check if the customer was created
        self.assertEqual(Customer.objects.first().name, 'Mohamed Ayman')
