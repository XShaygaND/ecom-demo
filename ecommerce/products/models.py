from django.db import models
from django.core.validators import MinValueValidator
from sellers.models import Seller

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    price = models.FloatField(validators=[MinValueValidator(0.01)])
    sales = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    sub_date = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)
    # in_warehouse = models.BooleanField(default=False)
    # warehouse = models.CharField(max_length=99, choices=warehouses, default=None)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __bool__(self):
        return self.is_active
