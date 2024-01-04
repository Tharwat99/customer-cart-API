from django.db import models
from django.utils.translation import gettext_lazy as _
from product.models import Product

class Cart(models.Model):
    """
    Cart Model related to customer one to one rel.
    """
    customer = models.OneToOneField('customer.Customer', on_delete=models.CASCADE, verbose_name = _('customer'))

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
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name = _('cart'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = _('product'))
    quantity = models.PositiveIntegerField(verbose_name = _('quantity'))
    status = models.PositiveSmallIntegerField(null = True, blank = True, choices=ITEM_STATUS, default = ADDED, verbose_name = _('status'))
    created_at = models.DateTimeField(auto_now_add=True, db_index = True, verbose_name = _('created_at'))
    updated_at = models.DateTimeField(auto_now=True, db_index = True, verbose_name = _('updated_at'))
    
    class Meta:
        ordering = ['-updated_at']
        
    def __str__(self):
        return self.product.name
    
