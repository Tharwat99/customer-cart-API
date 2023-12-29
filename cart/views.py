from django.db.models import Sum, F
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from product.models import Product
from .models import Cart, CartItem
from .serializers import CartListSerializer, CartCreateSerializer, CartItemSerializer


class CartListView(generics.ListAPIView):
    """
    View to list all serilized carts in form of CartListSerializer.
    """
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer

class CartCreateView(generics.CreateAPIView):
    """
    View to create Cart for customer in form of CartCreateSerializer.
    """
    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer


@extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'cart_id': {'type': 'integer'},
                'product_id': {'type': 'integer'},
                'quantity': {'type': 'integer'},
            },
            'required': ['cart_id', 'product_id', 'quantity'],
        },
    },
    responses={
        200: CartItemSerializer, 
        201: CartItemSerializer, 
        400: OpenApiResponse(response= 300, description="Bad Request",
            examples= [
                OpenApiExample(name="Example 1",description="Quantity for item added less than zero",
                value= {"error":"quantity must be more than zero."}
                ),
                OpenApiExample(name="Example 2",description="Item added stock less than quantity",
                value= {"error":"Insufficient stock quantity."}
                ),
        ]),
        404: {'type': 'object', 'properties': {'error': {'type': 'string', 'default':'Invalid cart or product.'}}},        
    },
    description='View to add item product to cart and check if...',
)
@api_view(['POST'])
def add_to_cart(request):
    """
    View to add item product to cart and check if
     - quantity greater than zero    
     - cart and product already exists
     - product stock greater than or equal quantity
     - product already added before than override it with new quantity.
    """
    cart_id = request.data.get('cart_id', None)
    product_id = request.data.get('product_id', None)
    quantity = int(request.data.get('quantity', '0'))

    # check if quantity less than zero then error message
    if quantity <= 0:
        return Response({'error': 'quantity must be more than zero'}, status=status.HTTP_400_BAD_REQUEST)
    # check if cart and product already exists
    try:
        cart = Cart.objects.get(id=cart_id)
        product = Product.objects.get(id=product_id)
    except (Cart.DoesNotExist, Product.DoesNotExist):
        return Response({"error": "Invalid cart or product."}, status=status.HTTP_404_NOT_FOUND)
    # check if product stock greater than or equal quantity
    if product.stock_quantity < quantity:
        return Response({'error': 'Insufficient stock quantity.'}, status=status.HTTP_400_BAD_REQUEST)
    # check if product already added before update it and override new quantity
    try:
        cart_item = CartItem.objects.get(cart =cart, product = product)
        cart_item.quantity = quantity
        cart_item.save()
        status_code = status.HTTP_200_OK
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        status_code = status.HTTP_201_CREATED
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status_code)

@api_view(['POST'])
def remove_from_cart(request):
    """
    View to remove item product from cart and check if
     - cart item already exists.
    """
    cart_item_id = request.data.get('cart_item_id', None)

    try:
        cart_item = CartItem.objects.get(id=cart_item_id, ordered = False)
    except CartItem.DoesNotExist:
        return Response({"error": "Invalid cart item."}, status=status.HTTP_404_NOT_FOUND)
    cart_item.delete()
    return Response({'message': 'Product removed from cart'})

@api_view(['POST'])
def update_cart_item_quantity(request):
    """
    View to update quantity for  item product in cart and check if
     - cart item already exists.
     - new quantity greater than 0
     - product stock not have enough amount.
    """

    cart_item_id = request.data.get('cart_item_id', None)
    new_quantity = int(request.data.get('quantity', 0))
    if new_quantity < 0:
        return Response({'error': 'Quantity must be more than zero'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, ordered=False)
    except CartItem.DoesNotExist:
        return Response({"error": "Invalid cart item."}, status=status.HTTP_404_NOT_FOUND)
    
    product = cart_item.product

    if product.stock_quantity < new_quantity:
        return Response({'error': 'Insufficient stock quantity'})

    product.stock_quantity += cart_item.quantity - new_quantity
    product.save()

    cart_item.quantity = new_quantity
    cart_item.save()

    return Response({'message': 'Cart item quantity updated'})

@api_view(['POST'])
def cart_checkout(request):
    """
    View to checkout orderitems in cart and update ordered to true and check if
     - cart  already exists.
     - new quantity greater than 0
     - product stock not have enough amount.
    """
    cart_id = request.data.get('cart_id', None)
    
    cart_order_items = CartItem.objects.filter(cart_id = cart_id, ordered = False).all()
    if len(cart_order_items)==0:
        return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        for cart_item in cart_order_items:
            cart_item.ordered = True
            cart_item.save()
            product = cart_item.product
            product.stock_quantity -= cart_item.quantity
            product.save()
    return Response({'message': 'Cart checked out.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def cart_details(request):
    """
    View to return cart details for all orders products, count, and total price if
     - cart  already exists.
    """
    cart_id = request.data.get('cart_id', None)
    cart_items = CartItem.objects.prefetch_related('product').filter(cart_id = cart_id, ordered=False)
    if len(cart_items) == 0:
        return Response({"error": "Invalid cart id."}, status=status.HTTP_404_NOT_FOUND)
    result = dict()
    result['cart_items'] = CartItemSerializer(cart_items, many=True).data
    result['count'] = cart_items.aggregate(count=Sum('quantity'))['count']
    result['total_price'] =  cart_items.aggregate(total_price=Sum(F('product__price') * F('quantity')))['total_price']
    return Response(result, status=status.HTTP_200_OK)