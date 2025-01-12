from django.contrib import admin

from .models import Seller
from .forms import SellerForm

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    form = SellerForm

    list_display = (
        'name',
        'description',
        'owner',
        'join_date',
        'sales',
        'slug',
        'is_active'
    )

    search_fields = ('name', 'description')
    readonly_fields = ('join_date', 'sales', 'slug')
