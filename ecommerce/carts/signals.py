from django.db.models.signals import pre_save, post_save, post_delete
from django.core.exceptions import ValidationError
from django.dispatch import receiver

from .models import Cart, CartItem


@receiver(pre_save, sender=Cart)
def cart_pre_save(sender, instance, **kwargs):
    if instance.pk is None:
        user = instance.owner
        if not (user.is_staff or user.is_superuser or user.is_seller):
            if Cart.objects.filter(owner=user).exists():
                raise ValidationError("A default user can only have one cart.")


@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_cart_count(sender, instance, **kwargs):
    instance.cart.update_count()
