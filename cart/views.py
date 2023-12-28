from rest_framework import generics
from .models import Cart
from .serializers import CartListSerializer, CartCreateSerializer


class CartListView(generics.ListCreateAPIView):
    """
    View to list all serilized carts in form of CartListSerializer.
    """
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer

class CartCreateView(generics.ListCreateAPIView):
    """
    View to create Cart for customer in form of CartCreateSerializer.
    """
    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer