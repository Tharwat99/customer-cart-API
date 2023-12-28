from rest_framework import serializers
from .models import Cart, CartItem
from customer.serializers import CustomerListSerializer
from product.serializers import ProductListSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'


class CartListSerializer(serializers.ModelSerializer):
    customer = CustomerListSerializer()
    cartitem_set = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = '__all__'

class CartCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    customer = CustomerListSerializer()
    cartitem_set = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'

