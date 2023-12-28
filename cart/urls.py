from django.urls import path
from .views import CartListView, CartCreateView, add_to_cart
urlpatterns = [
    path('cart-list/',CartListView.as_view(), name='cart_list'),
    path('cart-create/',CartCreateView.as_view(), name='cart_create'),
    path('add-item/',add_to_cart, name='add_item_to_cart'),
]