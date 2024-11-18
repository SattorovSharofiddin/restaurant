from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from apps.managers import CustomUserManager


class Customer(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = CustomUserManager()


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    @cached_property
    def total_price(self):
        return sum([product.price for product in self.products.all()])
