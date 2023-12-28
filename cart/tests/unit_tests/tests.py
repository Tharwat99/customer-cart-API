from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from cart.models import Cart
from customer.models import Customer

class CartListCreateViewTestCase(TestCase):
    """
    Test Cases for list and create Cart.
    """
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('cart_list')
        self.create_url = reverse('cart_create')

    def test_list_carts(self):
        # Create some carts with linked customers for testing
        user1 = Customer.objects.create(name='Ali')
        user2 = Customer.objects.create(name='Hassan')
        Cart.objects.create(customer = user1)
        Cart.objects.create(customer = user2)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check the number of carts returned

    def test_create_cart(self):
        # Create some carts for testing
        user1 = Customer.objects.create(name='Ali')
        data = {'customer': user1.id}

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)  # Check if the cart was created
        self.assertEqual(Cart.objects.first().customer.name, 'Ali')
