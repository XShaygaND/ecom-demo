from django.contrib import admin

from products.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'seller',
        'price',
        'stock',
        'sales',
        'sub_date',
        'is_active',
        )

    list_filter = ('seller',)
    search_fields = ('name', 'description')
    readonly_fields = ('sales', 'sub_date')

    def get_exclude(self, request, obj = ...):
        return ('sales',)
