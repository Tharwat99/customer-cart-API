from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from cart.models import Cart

class Customer(models.Model):
    """
    Customer Model.
    """
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Customer)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a Cart when a new User is created.
    """
    if created:
        Cart.objects.create(customer=instance)

# Connect the signal
post_save.connect(create_cart_for_new_user, sender=Customer)