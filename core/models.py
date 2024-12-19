from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, default="012345678", blank=True, null=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_addresses')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField()
    zip_code = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city}, {self.state}"

class CardDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_card_details')
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"Card details for {self.user.username}"