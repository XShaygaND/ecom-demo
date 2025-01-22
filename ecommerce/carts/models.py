from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product


User = get_user_model()

class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def update_count(self):
        total_quantity = self.cartitems.aggregate(total=models.Sum('quantity'))['total'] or 0
        self.count = total_quantity
        self.save()

    def __str__(self):
        return ', '.join((str(self.owner),  str(self.count), str(self.is_active)))

    def __bool__(self):
        return self.is_active


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

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
