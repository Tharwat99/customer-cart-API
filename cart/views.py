from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product
from .models import Cart, CartItem
from .serializers import CartListSerializer, CartCreateSerializer, CartItemSerializer


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


@api_view(['POST'])
def add_to_cart(request):
    """
    View to add item product to cart and check if
     - quantity greater than zero    
     - cart and product already exists
     - product stock greater than zero.
    """
    cart_id = request.data.get('cart_id', None)
    product_id = request.data.get('product_id', None)
    quantity = int(request.data.get('quantity'))

    if quantity <= 0:
        return Response({'error': 'Quantity must be more than zero'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        cart = Cart.objects.get(id=cart_id)
        product = Product.objects.get(id=product_id)
    except (Cart.DoesNotExist, Product.DoesNotExist):
        return Response({"error": "Invalid cart or product."}, status=status.HTTP_400_BAD_REQUEST)
    
    if product.stock_quantity < quantity:
        return Response({'error': 'Insufficient stock quantity'}, status=status.HTTP_400_BAD_REQUEST)
    
    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

