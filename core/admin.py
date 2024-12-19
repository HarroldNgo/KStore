from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address, CardDetails
from django import forms


# Inlines for related models
class AddressInline(admin.StackedInline):
    model = Address
    extra = 1
    classes = ['collapse']

class CardDetailsInline(admin.StackedInline):
    model = CardDetails
    extra = 1
    classes = ['collapse']

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'phone', 'is_staff', 'is_active')}
         ),
    )
    inlines = [AddressInline, CardDetailsInline]

class AddressAdmin(admin.ModelAdmin):
    search_fields = ['city', 'state', 'address', 'zip_code', 'user__username', 'user__email', 'user__first_name', 'user__last_name']
class CardDetailsAdmin(admin.ModelAdmin):
    search_fields = ['card_number', 'expiration_date', 'cvv', 'user__username', 'user__email', 'user__first_name', 'user__last_name']

admin.site.register(Address, AddressAdmin)
admin.site.register(CardDetails, CardDetailsAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
