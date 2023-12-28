from rest_framework import generics
from .models import Customer
from .serializers import CustomerListSerializer, CustomerCreateSerializer

class CustomerListCreateView(generics.ListAPIView):
    """
    View to list all serilized customer in form of CustomerListSerializer.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer


class CustomerListCreateView(generics.CreateAPIView):
    """
    View to create customer in form of CustomerCreateSerializer.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer
