from django.db import models
from django.utils.translation import gettext_lazy as _
from product.models import Product

class Cart(models.Model):
    """
    Cart Model.
    """
    customer = models.OneToOneField('customer.Customer', on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.name

class CartItem(models.Model):
    """
    CartItem Model.
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
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.PositiveSmallIntegerField(null = True, blank = True, choices=ITEM_STATUS, default = ADDED)
    created_at = models.DateTimeField(auto_now_add=True, db_index = True)
    updated_at = models.DateTimeField(auto_now=True, db_index = True)
    
    class Meta:
        ordering = ['-updated_at']
        
    def __str__(self):
        return self.product.name
    
