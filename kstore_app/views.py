import requests.exceptions
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

from .models import Item, Cart, CartItem
from .serializers import ItemSerializer, CartItemSerializer, SimpleCartSerializer, CartSerializer, UserSerializer, \
    UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(["GET"])
def items(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def item_detail(request, slug):
    item = Item.objects.get(slug=slug)
    serializer = ItemSerializer(item)
    return Response(serializer.data)

@api_view(["POST"])
def add_to_cart(request):
    try:
        cart_code = request.data.get("cart_code")
        item_id = request.data.get("item_id")
        quantity = request.data.get("quantity")
        quantity = int(quantity)
        cart, created = Cart.objects.get_or_create(cart_code = cart_code)

        if request.user.is_authenticated:
            cart.user =request.user

        item = Item.objects.get(id=item_id)

        cartItem, created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not created:
            cartItem.quantity += quantity
        else:
            cartItem.quantity = quantity
        cartItem.save()

        serializer = CartItemSerializer(cartItem)

        return Response({"data": serializer.data, "message": "CartItem created successfully"}, status=201)
    except Exception as e:
        return Response({"error":str(e)}, status=400)



@api_view(['GET'])
def get_cart_info(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    serializer = SimpleCartSerializer(cart)
    return Response(serializer.data)

@api_view(['GET'])
def get_cart(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['PATCH'])
def update_quantity(request):
    try:
        cartitem_id = request.data.get("item_id")
        quantity = request.data.get("quantity")
        quantity = int(quantity)
        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({"data": serializer.data, "message": "Cartitem updated successfully!"}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
def delete_item(request):
    cartitem_id = request.data.get("item_id")
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return Response({"mesaage": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    return Response({"username": user.username})



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def is_superuser(request):
    user = request.user
    return Response({"is_superuser": user.is_superuser})

@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    if request.user:
        current_count = cache.get(request.user.id, 0)
        current_count += 1
        cache.set(request.user.id, current_count, timeout=None)

        if current_count % 3 == 0:
            return Response({"detail": "Payment request denied. Try again later."}, status=403)

        cart_code = request.data.get("cart_code")
        cart = Cart.objects.get(cart_code=cart_code)
        cart.paid = True
        cart.user = request.user
        cart.save()

        for cartItem in cart.items.all():
            item = cartItem.item
            item.stock -= cartItem.quantity
            item.save()

        return Response({"detail": "Payment was successfully."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sync_cart(request):
    """
    Syncs the session cart with the authenticated user's cart.
    """
    try:
        cart_code = request.data.get("cart_code")
        user = request.user

        # Get the session cart (from cart_code)
        session_cart = Cart.objects.filter(cart_code=cart_code, paid=False).first()
        # Get the authenticated user's existing cart
        user_cart = Cart.objects.filter(user=user, paid=False).first()

        if session_cart and user_cart:
            # Merge carts: add session cart items to user cart
            for item in session_cart.items.all():
                user_cart_item, created = CartItem.objects.get_or_create(
                    cart=user_cart,
                    item=item.item,
                    defaults={"quantity": item.quantity}
                )
                if not created:
                    user_cart_item.quantity += item.quantity
                    user_cart_item.save()
            # Delete session cart after merging
            session_cart.delete()

        elif session_cart:
            # Assign the session cart to the user if no user cart exists
            session_cart.user = user
            session_cart.save()

        # Use the user's cart if it exists, otherwise fallback to session cart
        cart = user_cart or session_cart
        if not cart:
            return Response({"detail": "No cart found to sync."}, status=404)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    try:
        user = request.user

        user.username = request.data.get("username")
        user.first_name = request.data.get("first_name")
        user.last_name = request.data.get("last_name")
        user.email = request.data.get("email")
        user.phone = request.data.get("phone")

        addresses = request.data.get("addresses")
        user_address = user.user_addresses.first()
        user_address.city = addresses.get("city")
        user_address.state = addresses.get("state")
        user_address.address = addresses.get("address")
        user_address.zip_code = addresses.get("zip_code")
        user_address.save()

        card_details = request.data.get("card_details")
        user_card_details = user.user_card_details.first()
        user_card_details.card_number = card_details.get("card_number")
        user_card_details.expiration_date = card_details.get("expiration_date")
        user_card_details.cvv = card_details.get("cvv")
        user_card_details.save()

        user.save()
        serializer = UserSerializer(user)
        return Response({"data": serializer.data, "message": "User updated successfully!"}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)
