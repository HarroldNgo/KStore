from django.contrib import admin
from .models import Item, Cart, CartItem

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description', 'flavour', 'category']
class CartAdmin(admin.ModelAdmin):
    search_fields = ['cart_code', 'user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_filter = ['paid']
class CartItemAdmin(admin.ModelAdmin):
    search_fields = ['cart__cart_code','cart__user__username', 'cart__user__email', 'cart__user__first_name', 'cart__user__last_name',
                     'item__name', 'item__description', 'item__flavour', 'item__category' ]
    list_filter = ['cart__paid']

admin.site.register(Item, ItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)