from django.urls import path
from .views import (
    CartListView,
    CartCreateView,
    add_to_cart,
    remove_from_cart,
    update_cart_item_quantity,
    cart_checkout,
    cart_details
)
urlpatterns = [
    path('cart-list/', CartListView.as_view(), name='cart_list'),
    path('cart-create/', CartCreateView.as_view(), name='cart_create'),
    path('add-item/', add_to_cart, name='add_item_to_cart'),
    path('remove-item/', remove_from_cart, name='remove_item_from_cart'),
    path('update-item-quantity/', update_cart_item_quantity, name='update_cart_item_quantity'),
    path('cart-checkout/', cart_checkout, name='cart_checkout'),
    path('cart-details/', cart_details, name='cart_details')
]