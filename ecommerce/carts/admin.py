from django.contrib import admin

from .models import Cart, CartItem
from .forms import CartAdminForm, CartItemAdminForm


class CartItemInline(admin.TabularInline):
    model = CartItem
    form = CartItemAdminForm
    extra = 0

    fields = ["product", 'product_price', "quantity"]
    readonly_fields = ['product_price',]

    @staticmethod
    def product_price(obj):
        return obj.product.price


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    form = CartAdminForm

    list_display = (
        'id',
        'is_active',
        'total_sum',
        'owner',
        'count',
    )

    list_filter = ('is_active',)
    search_fields = ('id', 'owner__email')
    readonly_fields = ('total_sum',  'count')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    form = CartItemAdminForm

    list_display = (
        'id',
        'cart',
        'product',
        'quantity',
    )

    list_filter = ('cart',)
    search_fields = ('id', 'cart__owner__email', 'product__name')
