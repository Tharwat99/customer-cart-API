from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from product.models import Product
from customer.models import Customer
from cart.models import Cart, CartItem
class YourAppFunctionalTest(TestCase):
    """
    Functional Cases for cart operations.
    """
    def setUp(self):
        self.client = APIClient()
        self.add_item_to_cart = reverse('cart-add-item')
        self.remove_item_from_cart = reverse('cart-remove-item')
        self.update_cart_item_quantity = reverse('cart-update-item-quantity')
        self.cart_checkout = reverse('cart-checkout-items')
        self.cart_details = reverse('cart-checkout-items')

        # Create some products
        self.product1 = Product.objects.create(name='Product 1', price=10.0, stock_quantity=15)
        self.product2 = Product.objects.create(name='Product 2', price=15.0, stock_quantity=20)
        # Create customer
        self.customer = Customer.objects.create(name='Customer 1')

    def test_add_products_checkout(self):
        # Add products to the cart
        data = {
            'cart': self.customer.cart.id,
            'product': self.product1.id,
            'quantity': 5,
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'cart': self.customer.cart.id,
            'product': self.product2.id,
            'quantity': 7,
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'cart_id': self.customer.cart.id
        }
        self.assertEqual(self.customer.cart.cartitem_set.filter(status=CartItem.ADDED).count(), 2)
        response = self.client.post(self.cart_checkout, data)
        self.customer.cart.refresh_from_db()
        self.assertEqual(self.customer.cart.cartitem_set.filter(status=CartItem.ADDED).count(), 0)
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        # check that products stock updated after checkout
        self.assertEqual(self.product1.stock_quantity, 10)
        self.assertEqual(self.product2.stock_quantity, 13)
    
       
        