from django.urls import path
from .views import CartListView, CartCreateView
urlpatterns = [
    path('cart-list/',CartListView.as_view(), name='cart_list'),
    path('cart-create/',CartCreateView.as_view(), name='cart_create'),
]