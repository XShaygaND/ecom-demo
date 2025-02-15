from django import forms
from django.core.exceptions import ValidationError

from decimal import Decimal

from .models import Cart, CartItem

class CartAdminForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'

    def clean_total_sum(self):
        total_sum = self.cleaned_data.get('total_sum')

        if total_sum >= Decimal('1000000000.00'):
            raise ValidationError("Total sum exceeds the maximum allowed value.")

        return total_sum


class CartItemAdminForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'

    def clean_cart(self):
        cleaned_data = super().clean()
        cart = cleaned_data.get('cart')

        if not cart.is_active:
            raise ValidationError("Cannot add items to an inactive cart.")

        return cleaned_data
