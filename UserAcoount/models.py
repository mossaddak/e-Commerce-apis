import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomeUserManager


# Create your models here.
class User(AbstractUser):
    SELLER = "Seller"
    BUYER = "Buyer"
    ACCOUNT_TYPE_CHOICES = [(SELLER, "Seller"), (BUYER, "Buyer")]
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(
        max_length=50,
        unique=True,
        null=False,
        error_messages={"unique": "the email must be unique"},
    )
    user_type = models.CharField(
        max_length=50, choices=ACCOUNT_TYPE_CHOICES, default=BUYER
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomeUserManager()

    def __str__(self):
        return f"{self.uid}.{self.email}"


class Address(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Addresses")
    post_office = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.uid}.{self.user}"
