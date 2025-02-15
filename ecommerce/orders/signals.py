from django.db.models.signals import pre_save, post_save, post_delete
from django.core.exceptions import ValidationError
from django.dispatch import receiver

from .models import Order


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    if not instance.pk and not instance.cart.cartitems.exists():
        raise ValidationError("Cart can not be empty for order creaiton.")
    instance.total_sum = instance.cart.total_sum

@receiver(post_save, sender=Order)
def order_post_save(sender, created,  instance, **kwargs):
    if created:
        instance.cart.is_active = False
        instance.cart.save()