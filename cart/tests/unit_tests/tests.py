from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from cart.models import Cart, CartItem
from customer.models import Customer
from product.models import Product

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

class CartAddItemViewTest(TestCase):
    """
    Test Cases for add item to cart.
    """
    def setUp(self):
        # Create test data
        self.client = APIClient()
        self.customer = Customer.objects.create(name='Hassan')
        self.cart = Cart.objects.create(customer = self.customer)
        self.product = Product.objects.create(name='Test Product', price = 500, stock_quantity=10)
        self.exists_product = Product.objects.create(name='Test Product', price = 500, stock_quantity=10)
        self.exists_cart_item = CartItem.objects.create(cart=self.cart, product=self.exists_product, quantity=5) 
        self.add_item_to_cart = reverse('add_item_to_cart')
        
    def test_add_to_cart_success(self):
        data = {
            'cart_id': self.cart.id,
            'product_id': self.product.id,
            'quantity': 5,
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
    
    def test_update_already_exists_product_cart_success(self):
        data = {
            'cart_id': self.cart.id,
            'product_id': self.exists_product.id,
            'quantity': 3,
        }
        self.exists_cart_item 
        self.assertEqual(self.exists_cart_item.quantity, 5)
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.exists_cart_item.refresh_from_db()
        self.assertEqual(self.exists_cart_item.quantity, 3)
        

    def test_add_to_cart_invalid_quantity(self):
        data = {
            'cart_id': self.cart.id,
            'product_id': self.product.id,
            'quantity': 0,
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_add_to_cart_invalid_cart_or_product(self):
        data = {
            'cart_id': 999,  # Invalid cart_id
            'product_id': self.product.id,
            'quantity': 5,
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_add_to_cart_insufficient_stock(self):
        data = {
            'cart_id': self.cart.id,
            'product_id': self.product.id,
            'quantity': 15,  # Quantity exceeds stock
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
class CartRemoveItemViewTest(TestCase):
    """
    Test Cases for remove item from cart.
    """
    def setUp(self):
        # Create test data
        self.client = APIClient()
        item_quantity = 3
        self.customer = Customer.objects.create(name='Hassan')
        self.cart = Cart.objects.create(customer = self.customer)
        self.product = Product.objects.create(name='Test Product', price = 500, stock_quantity=10)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=item_quantity)
        self.product.stock_quantity -= item_quantity
        self.product.save()
        self.remove_item_from_cart = reverse('remove_item_from_cart')
        
    def test_remove_from_cart_success(self):
        data = {
            'cart_item_id': self.cart_item.id,
        }
        response = self.client.post(self.remove_item_from_cart, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_remove_from_cart_invalid_cart_item(self):
        data = {
            'cart_item_id': 999,  # Invalid cart_item_id

        }
        response = self.client.post(self.remove_item_from_cart, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

class CartUpdateItemQuantityViewTest(TestCase):
    """
    Test Cases for update item quantity in cart.
    """
    def setUp(self):
        # Create test data
        self.client = APIClient()
        item_quantity = 3
        self.customer = Customer.objects.create(name='Hassan')
        self.cart = Cart.objects.create(customer = self.customer)
        self.product = Product.objects.create(name='Test Product', price = 500, stock_quantity=10)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=item_quantity)
        self.product.stock_quantity -= item_quantity
        self.product.save()
        self.update_cart_item_quantity = reverse('update_cart_item_quantity')
        
    def test_update_item_quantity_in_cart_success(self):
        data = {
            'cart_item_id': self.cart_item.id,
            'quantity': 5
        }
        self.assertEqual(self.product.stock_quantity, 7)
        response = self.client.post(self.update_cart_item_quantity, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 5)
    
    def test_update_item_quantity_invalid_value(self):
        data = {
            'cart_item_id': self.cart_item.id,
            'quantity': -1,
        }
        response = self.client.post(self.update_cart_item_quantity, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_remove_from_cart_invalid_cart_item(self):
        data = {
            'cart_item_id': 999,  # Invalid cart_item_id
            'quantity': 5
        }
        response = self.client.post(self.update_cart_item_quantity, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

class CartCheckoutViewTest(TestCase):
    """
    Test Cases for Cart Checkout view.
    """
    def setUp(self):
        # Create test data
        self.client = APIClient()
        item_quantity = 3
        self.customer = Customer.objects.create(name='Hassan')
        self.cart = Cart.objects.create(customer = self.customer)
        other_customer = Customer.objects.create(name='Hassan')
        self.empty_cart = Cart.objects.create(customer = other_customer)
        self.product = Product.objects.create(name='Test Product', price = 500, stock_quantity=10)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=item_quantity)
        self.product.stock_quantity -= item_quantity
        self.product.save()
        self.cart_checkout = reverse('cart_checkout')
        
    def test_cart_checkout_success(self):
        data = {
            'cart_id': self.cart.id
        }
        self.assertEqual(self.cart.cartitem_set.filter(ordered=False).count(), 1)
        response = self.client.post(self.cart_checkout, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.cartitem_set.filter(ordered=False).count(), 0)
    
    def test_cart_checkout_invalid_cart(self):
        data = {
            'cart_id': 999,  # Invalid cart_id
        }
        response = self.client.post(self.cart_checkout, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
    
    def test_cart_checkout_empty_cart(self):
        data = {
            'cart_id': self.empty_cart.id
        }
        response = self.client.post(self.cart_checkout, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)