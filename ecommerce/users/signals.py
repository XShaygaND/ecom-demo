from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from carts.models import Cart


user = get_user_model()

@receiver(post_save, sender=user)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)