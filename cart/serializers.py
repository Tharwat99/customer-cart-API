from django.db.models import Sum, F
from rest_framework import serializers
from .models import Cart, CartItem
from customer.serializers import CustomerListSerializer
from product.serializers import ProductListSerializer

class CartItemSerializer(serializers.ModelSerializer):
    """
    CartItem Serializer to serializer all data about cart items and associated products.
    """
    product = ProductListSerializer()
    class Meta:
        model = CartItem
        fields = '__all__'

class CartItemAddSerializer(serializers.ModelSerializer):
    """
    CartItemAdd Serializer to add item product to cart and check if
     - quantity greater than zero    
     - product has stock to add it that greater than quantity.
     - product already added before override it with new quantity
     - product already removed before overrid it with new quantity.
    """
    class Meta:
        model = CartItem
        fields = '__all__'
    
    def create(self, validated_data):
        try:
            cart_item = CartItem.objects.get(cart=validated_data['cart'], product=validated_data['product'], status__in = [CartItem.ADDED, CartItem.REMOVED])
            if cart_item.status == CartItem.REMOVED:
                cart_item.status = CartItem.ADDED
            cart_item.quantity = validated_data['quantity']
            cart_item.save()
            return cart_item
        except CartItem.DoesNotExist:
            return super().create(validated_data)
            
        
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be more than zero.")
        return value
    
    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']
        
        # Check if product stock is greater than or equal to quantity
        if product.stock_quantity < quantity:
            raise serializers.ValidationError("Insufficient stock quantity.")
        return attrs   
   
class CartItemRemoveSerializer(serializers.ModelSerializer):
    """
    CartItemRemove Serializer to update cartitem status to removed and check if
    - already removed before.
    """
    class Meta:
        model = CartItem
        fields = ['status']
    
    def update(self, instance, validated_data):
        if instance.status is CartItem.REMOVED:
            raise serializers.ValidationError({"status": ["Cart item Already Removed Before."]})
        instance.status = CartItem.REMOVED
        instance.save()
        return instance
    
class CartItemUpdateQuantitySerializer(serializers.ModelSerializer):
    """
    CartItemUpdateQuantity Serializer to update item product quantity and check if
     - quantity greater than zero 
     - product has stock to add it that greater than quantity.
    """
    class Meta:
        model = CartItem
        fields = ['quantity']
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
            
        
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be more than zero.")
        return value
    
    def validate(self, attrs):
        product = self.instance.product
        quantity = attrs['quantity']
        
        # Check if product stock is greater than or equal to quantity
        if product.stock_quantity < quantity:
            raise serializers.ValidationError("Insufficient stock quantity.")
        return attrs
        
class CartDetailSerializer(serializers.ModelSerializer):
    """
    CartDetailSerializer Serializer to serializer data about cart details
     - product items (cartitem_set)
     - count for all quantity for each product item
     - total price for cart items in cart. 
    """
    cartitem_set = CartItemSerializer(many= True)
    count = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['cartitem_set', 'count', 'total_price']
        
    def get_count(self, obj):
        return obj.cartitem_set.aggregate(count=Sum('quantity'))['count']

    def get_total_price(self, obj):
        return obj.cartitem_set.aggregate(total_price=Sum(F('product__price') * F('quantity')))['total_price']

