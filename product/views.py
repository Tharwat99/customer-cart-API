from rest_framework import generics
from .models import Product
from .serializers import ProductListSerializer, ProductCreateSerializer


class ProductListView(generics.ListAPIView):
    """
    View to list all serilized products in form of ProductListSerializer.
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class ProductCreateView(generics.CreateAPIView):
    """
    View to create Product in form of ProductCreateSerializer.
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer