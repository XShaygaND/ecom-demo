from django.db import models
from django.db.models import Sum, F
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from decimal import Decimal, ROUND_DOWN

from products.models import Product


User = get_user_model()

class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def update_totals(self):
        total_quantity = self.cartitems.aggregate(total=Sum('quantity'))['total'] or 0
        total_price = self.cartitems.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0.00

        total_price = Decimal(str(total_price)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

        if total_price >= Decimal('1000000000.00'):
            raise ValidationError("Total sum exceeds the maximum allowed value.")

        self.count = total_quantity
        self.total_sum = total_price
        self.save()

    def __str__(self):
        return ', '.join((str(self.owner),  str(self.count), str(self.is_active)))

    def __bool__(self):
        return self.is_active


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def clean(self):
        if not self.cart.is_active:
            raise ValidationError("Cannot add items to an inactive cart.")

    def save(self, *args, **kwargs):
        self.full_clean()

        existing_item = CartItem.objects.filter(cart=self.cart, product=self.product).exclude(pk=self.pk).first()

        if existing_item:
            existing_item.quantity += self.quantity
            CartItem.objects.filter(pk=existing_item.pk).update(quantity=existing_item.quantity)
            total_quantity = existing_item.cart.cartitems.aggregate(total=models.Sum('quantity'))['total'] or 0
            self.cart.count = total_quantity
            self.cart.save()

        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return 'Cart: (' + str(self.cart) + ') ,' + ', '.join([str(self.product), str(self.quantity)])
