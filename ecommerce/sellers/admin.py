from django.contrib import admin

from .models import Seller
from .forms import SellerForm

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    form = SellerForm

    list_display = (
        'id',
        'name',
        'description',
        'owner',
        'join_date',
        'sales',
        'slug',
        'is_active'
    )

    search_fields = ('name', 'owner__email')
    readonly_fields = ('join_date', 'sales', 'slug')
