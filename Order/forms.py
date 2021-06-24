from django import forms
from .models import *

class ShoppingCartForm(forms.ModelForm):
    class Meta:
        model = ShopCart
        fields = ['qty']

class ShoppingCartUpdateDeviceForm(forms.ModelForm):
    class Meta:
        model = ShopCartDevice
        fields = ['qty']

class ShoppingCartDeviceForm(forms.ModelForm):
    class Meta:
        model = ShopCartDevice
        fields = ['device', 'qty']

class OderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name',
                  'phone', 'address', 'city', 'country', 'transaction_id', 'transaction_image']