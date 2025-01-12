from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Seller(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    sales = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=100, unique=True, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
