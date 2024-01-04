from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from cart.models import Cart, CartItem
from customer.models import Customer
from product.models import Product

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
        self.add_item_to_cart = reverse('cart-add-item')
        
    def test_add_to_cart_success(self):
        data = {
            'cart': self.cart.id,
            'product': self.product.id,
            'quantity': 5,
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
    
    def test_update_already_exists_product_cart_success(self):
        data = {
            'cart': self.cart.id,
            'product': self.exists_product.id,
            'quantity': 3,
        }
        self.exists_cart_item 
        self.assertEqual(self.exists_cart_item.quantity, 5)
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.exists_cart_item.refresh_from_db()
        self.assertEqual(self.exists_cart_item.quantity, 3)
        

    def test_add_to_cart_invalid_quantity(self):
        data = {
            'cart': self.cart.id,
            'product': self.product.id,
            'quantity': 0,
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Quantity must be more than zero.', response.data['quantity'][0])


    def test_add_to_cart_invalid_cart_or_product(self):
        data = {
            'cart': 999,  # Invalid cart_id
            'product': self.product.id,
            'quantity': 5,
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_add_to_cart_insufficient_stock(self):
        data = {
            'cart': self.cart.id,
            'product': self.product.id,
            'quantity': 15,  # Quantity exceeds stock
        }
        response = self.client.post(self.add_item_to_cart, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
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
        self.remove_item_from_cart = reverse('cart-remove-item')
        
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
        self.customer = Customer.objects.create(name='Hassan')
        self.cart = Cart.objects.create(customer = self.customer)
        self.product = Product.objects.create(name='Test Product', price = 500, stock_quantity=10)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)
        self.update_cart_item_quantity = reverse('cart-update-item-quantity')
        
    def test_update_item_quantity_in_cart_success(self):
        data = {
            'cart_item_id': self.cart_item.id,
            'quantity': 5
        }
        response = self.client.post(self.update_cart_item_quantity, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_item_quantity_invalid_value(self):
        data = {
            'cart_item_id': self.cart_item.id,
            'quantity': -1,
        }
        response = self.client.post(self.update_cart_item_quantity, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Quantity must be more than zero.', response.data['quantity'][0])

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
        self.cart_checkout = reverse('cart-checkout-items')
        
    def test_cart_checkout_success(self):
        data = {
            'cart_id': self.cart.id
        }
        self.assertEqual(self.cart.cartitem_set.filter(status=CartItem.ADDED).count(), 1)
        response = self.client.post(self.cart_checkout, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.cartitem_set.filter(status=CartItem.ADDED).count(), 0)
    
    def test_cart_checkout_empty_cart(self):
        data = {
            'cart_id': self.empty_cart.id
        }
        response = self.client.post(self.cart_checkout, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class CartDetailsViewTest(TestCase):
    """
    Test Cases for Cart Details view.
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
        self.cart_details = reverse('cart-items-details')
        
    def test_cart_details_success(self):
        data = {
            'cart_id': self.cart.id
        }
        response = self.client.post(self.cart_details, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.cart.cartitem_set.filter(status=CartItem.ADDED).count(), 1)
    
    def test_cart_details_empty_cart(self):
        data = {
            'cart_id': 999 # Invalid cart_item_id
        }
        response = self.client.post(self.cart_details, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)