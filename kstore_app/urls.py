from django.urls import path, include
from . import views

urlpatterns = [
    path("items", views.items, name="items"),
    path("item_detail/<slug:slug>", views.item_detail, name="item_detail"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("get_cart_info", views.get_cart_info, name="get_cart_info"),
    path("get_cart", views.get_cart, name="get_cart"),
    path("update_quantity/", views.update_quantity, name="update_quantity"),
    path("delete_item/", views.delete_item, name="delete_item"),
    path("get_username", views.get_username, name="get_username"),
    path("is_superuser", views.is_superuser, name="is_superuser"),
    path("user_info", views.user_info, name="user_info"),
    path("register_user/", views.register_user, name="register_user"),
    path("update_user/", views.update_user, name="update_user"),

    path("sync_cart/", views.sync_cart, name="sync_cart"),

    path("initiate_payment/", views.initiate_payment, name="initiate_payment"),
]