from django.db import models
from django.core.exceptions import ValidationError

from carts.models import Cart


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        DELIVERED = "delivered", "Delivered"
        RETURNED = "returned", "Returned"
        CANCELED = "canceled", "Canceled"

    is_active = models.BooleanField(default=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    after_pay = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def clean(self):
        if self.pk and not self.is_active:
            raise ValidationError("Cannot modify an inactive Order.")

    def __str__(self):
        return ', '.join((str(self.cart), str(self.status), str(self.total_sum), str(self.after_pay)))
