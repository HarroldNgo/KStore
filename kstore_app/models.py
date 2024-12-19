from django.db import models
from django.utils.text import slugify
import uuid
from django.conf import settings

#Item Model
class Item(models.Model):
    CATEGORY = (("Macarons", "MACARONS"),
                ("Cupcakes", "CUPCAKES"),
                ("Cakes", "CAKES"),
                ("Cookies", "COOKIES"),
                ("Brownies", "BROWNIES"),
                ("Cake Pops", "CAKE POPS")
                )
    FLAVOUR = (("Vanilla", "VANILLA"),
               ("Chocolate", "CHOCOLATE"),
               ("Red Velvet", "RED VELVET"),
               ("Cookies & Cream", "COOKIES & CREAM"),
               )
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to="img")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=15, choices=CATEGORY, blank=True, null=True)
    flavour = models.CharField(max_length=15, choices=FLAVOUR, blank=True, null=True)
    stock = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    #Deals with duplicate slugs for url
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Start with the slugified name
            unique_slug = self.slug
            if Item.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{uuid.uuid4().hex[:6]}'  # Append a short UUID
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Cart(models.Model):
    cart_code = models.CharField(max_length=11, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.cart_code


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in cart {self.cart.id}"