from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from product.models import Product
from customer.models import Customer
from cart.models import Cart
class YourAppFunctionalTest(TestCase):
    """
    Functional Cases for cart operations.
    """
    def setUp(self):
        self.client = APIClient()
        self.add_item_to_cart = reverse('add_item_to_cart')
        self.remove_item_from_cart = reverse('remove_item_from_cart')
        self.update_cart_item_quantity = reverse('update_cart_item_quantity')
        self.cart_checkout = reverse('cart_checkout')
        self.cart_details = reverse('cart_details')

        # Create some products
        self.product1 = Product.objects.create(name='Product 1', price=10.0, stock_quantity=15)
        self.product2 = Product.objects.create(name='Product 2', price=15.0, stock_quantity=20)
        # Create customer
        self.customer = Customer.objects.create(name='Customer 1')
        # Create cart
        self.cart = Cart.objects.create(customer=self.customer)

    def test_add_products_checkout(self):
        # Add products to the cart
        data = {
            'cart_id': self.cart.id,
            'product_id': self.product1.id,
            'quantity': 5,
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'cart_id': self.cart.id,
            'product_id': self.product2.id,
            'quantity': 7,
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'cart_id': self.cart.id
        }
        self.assertEqual(self.cart.cartitem_set.filter(ordered=False).count(), 2)
        response = self.client.post(self.cart_checkout, data)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.cartitem_set.filter(ordered=False).count(), 0)
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        # check that products stock updated after checkout
        self.assertEqual(self.product1.stock_quantity, 10)
        self.assertEqual(self.product2.stock_quantity, 13)
    
       
        