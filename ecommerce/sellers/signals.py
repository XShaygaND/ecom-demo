from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
from django.dispatch import receiver

from .models import Seller

@receiver(pre_save, sender=Seller)
def seller_pre_save(sender, instance, **kwargs):
    if not instance.owner.is_seller:
        raise ValueError("Seller's owner must have it's 'is_seller' set as True.")

    elif not instance.pk and Seller.objects.filter(slug=instance.name.lower()).exists():
        raise ValueError("Seller with such name already exists.")

@receiver(post_save, sender=Seller)
def update_seller_slug(sender, instance, created, **kwargs):
    if created:
        slug = slugify(instance.name)
        instance.slug = slug.lower()
        instance.save()
