from django.db import models
from django.utils.translation import gettext_lazy as _
from product.models import Product

class Cart(models.Model):
    """
    Cart Model related to customer one to one rel.
    """
    customer = models.OneToOneField('customer.Customer', on_delete=models.CASCADE, verbose_name = _('Customer'))
    
    class Meta:
        ordering = ['-id']
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        
    def __str__(self):
        return self.customer.name

class CartItem(models.Model):
    """
    CartItem Model for each product added to cart with specific quantity
    """
    ADDED = 0
    REMOVED = 1
    CHECKOUT = 2

    # status for item in cart
    ITEM_STATUS = (
        (ADDED, _('Item Added')),
        (REMOVED, _('Item Removed')),
        (CHECKOUT, _('Item Checkout')),
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name = _('Cart'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = _('Product'))
    quantity = models.PositiveIntegerField(verbose_name = _('Quantity'))
    status = models.PositiveSmallIntegerField(null = True, blank = True, choices=ITEM_STATUS, default = ADDED, verbose_name = _('status'))
    created_at = models.DateTimeField(auto_now_add=True, db_index = True, verbose_name = _('Created at'))
    updated_at = models.DateTimeField(auto_now=True, db_index = True, verbose_name = _('Updated at'))
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def __str__(self):
        return self.product.name
    
