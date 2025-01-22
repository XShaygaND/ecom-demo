from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'is_active',
        'owner',
        'count',
    )

    list_filter = ('is_active',)
    search_fields = ('owner__email',)
    readonly_fields = ('count',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'product',
        'quantity',
    )

    list_filter = ('cart',)
    search_fields = ('id', 'cart__owner__email', 'product__name')
