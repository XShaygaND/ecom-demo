from django import forms
from django.core.exceptions import ValidationError
from .models import Seller


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        owner = cleaned_data.get('owner')
        if not owner.is_seller:
            raise ValidationError("Seller's owner must have 'is_seller' set to True.")

        elif Seller.objects.filter(slug=cleaned_data.get('name').lower()).exists():
            raise ValidationError("Seller with such name already exists.")
        return cleaned_data