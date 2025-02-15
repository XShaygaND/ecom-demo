from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'total_sum',
        'cart',
        'status',
        'after_pay',
    )

    list_filter = (
        'status',
        'after_pay',
    )
    search_fields = (
        'id',
        # 'cart__cartitems__product__name',
        # 'cart__cartitems__product__seller',
        'cart__owner__email',
    )
    readonly_fields = ('total_sum', 'cart', 'after_pay')
