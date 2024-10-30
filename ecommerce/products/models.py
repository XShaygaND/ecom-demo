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
    in_warehouse = models.BooleanField(default=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    # warehouse = models.CharField(max_length=99, choices=warehouses, default=None)

    def __str__(self):
        return self.name
