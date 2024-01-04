from django.db.models import Sum, F
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view,action

from django.db.models import Prefetch
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import (
    CartItemSerializer, 
    CartItemAddSerializer, 
    CartItemRemoveSerializer, 
    CartItemUpdateQuantitySerializer, 
    CartDetailSerializer
)
class CartViewSet(viewsets.GenericViewSet):
    """
    View set to apply operations on cart 
     - add product item to cart.
     - remove product item from cart.
     - update quantity for product item in cart.
     - checkout product items in cart.
     - show details about cart
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    @action(methods=['POST'], detail=False)
    def add_item(self, request):
        serializer = CartItemAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['POST'], detail=False)
    def remove_item(self, request):
        cart_item_id = request.data.get('cart_item_id', None)
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Invalid cart item."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemRemoveSerializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Remove Successfully", status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False)
    def update_item_quantity(self, request):
        cart_item_id = request.data.get('cart_item_id', None)
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, status=CartItem.ADDED)
        except CartItem.DoesNotExist:
            return Response({"error": "Invalid cart item."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemUpdateQuantitySerializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.get_serializer(cart_item).data)
    
    @action(methods=['POST'], detail=False)
    def checkout_items(self, request):
        cart_id = request.data.get('cart_id', None)
        cart_order_items = CartItem.objects.filter(cart_id = cart_id, status = CartItem.ADDED).all()
        if len(cart_order_items)==0:
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            for cart_item in cart_order_items:
                cart_item.status = CartItem.CHECKOUT
                cart_item.save()
                product = cart_item.product
                product.stock_quantity -= cart_item.quantity
                product.save()
        return Response({'message': 'Cart checked out.'}, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False)
    def items_details(self, request):
        cart_id = request.data.get('cart_id', None)
        try:
            cart = Cart.objects.select_related('customer').prefetch_related(Prefetch('cartitem_set', queryset=CartItem.objects.select_related('product'))).get(pk=cart_id)
        except Cart.DoesNotExist:
            return Response({"error": "Empty cart."}, status=status.HTTP_404_NOT_FOUND)
        return Response(CartDetailSerializer(cart).data, status=status.HTTP_200_OK)
