from rest_framework import serializers
from .models import Item, Cart, CartItem
from django.contrib.auth import get_user_model
from core.models import Address, CardDetails

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "slug", "image", "description", "category", "flavour", "price", "stock"]

class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ["id", "quantity", "item", "total"]
    def get_total(self, cartitem):
        price = cartitem.item.price * cartitem.quantity
        return price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)
    sum_total = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()
    num_of_distinct_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ["id", "cart_code", "items", "sum_total", "num_of_distinct_items", "num_of_items", "created_at", "modified_at"]

    def get_sum_total(self, cart):
        items = cart.items.all()
        total = sum([item.item.price * item.quantity for item in items])
        return total

    def get_num_of_items(self, cart):
        items = cart.items.all()
        total = sum([item.quantity for item in items])
        return total

    def get_num_of_distinct_items(self, cart):
        item_ids = CartItem.objects.filter(cart=cart).values_list("item_id", flat=True)
        item_count = item_ids.distinct().count()
        return item_count

class SimpleCartSerializer(serializers.ModelSerializer):
    num_of_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ["id", "cart_code", "num_of_items"]

    def get_num_of_items(self, cart):
        num_of_items = sum([item.quantity for item in cart.items.all()])
        return num_of_items


class OrderedCartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    order_id = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "item", "quantity", "order_id", "order_date"]

    def get_order_id(self, cartitem):
        order_id = cartitem.cart.cart_code
        return order_id

    def get_order_date(self, cartitem):
        order_date = cartitem.cart.modified_at
        return order_date

# Serializer for Address model
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'city', 'state', 'address', 'zip_code']


# Serializer for CardDetails model
class CardDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDetails
        fields = ['id', 'card_number', 'expiration_date', 'cvv']

class UserSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    user_addresses = AddressSerializer(many=True, read_only=True)
    user_card_details = CardDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "phone", "user_addresses", "user_card_details", "items", "is_superuser"]

    def get_items(self, user):
        cartitems = CartItem.objects.filter(cart__user=user, cart__paid=True)
        serializer = OrderedCartItemSerializer(cartitems, many=True)
        return serializer.data


class UserRegistrationSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(required=False, allow_null=True)
    card_details = CardDetailsSerializer(required=False, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "password", "phone", "addresses", "card_details"]
        extra_kwargs = {
            'password': {'write_only': True},
            "phone": {"required": False, "allow_blank": True}
        }

    def create(self, validated_data):
        address_data = validated_data.get("addresses", None)
        card_details_data = validated_data.get("card_details", None)
        print(address_data)
        print(card_details_data)

        username = validated_data["username"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        password = validated_data["password"]
        phone = validated_data.get("phone", None)
        email = validated_data["email"]

        user = get_user_model()
        new_user = user.objects.create(username=username,
                                       first_name=first_name,
                                       last_name=last_name,
                                       phone=phone,
                                       email=email)
        new_user.set_password(password)
        new_user.save()

        if address_data:
            print(address_data)
            new_address = Address.objects.create(
                user=new_user,
                city=address_data.get("city"),
                state=address_data.get("state"),
                address=address_data.get("address"),
                zip_code=address_data.get("zip_code")
            )
            new_address.save()

        if card_details_data:
            print(card_details_data)
            new_card_details = CardDetails.objects.create(
                user=new_user,
                card_number=card_details_data.get("card_number"),
                expiration_date=card_details_data.get("expiration_date"),
                cvv=card_details_data.get("cvv")
            )
            new_card_details.save()

        return new_user
