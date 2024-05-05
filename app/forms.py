# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class ShopRegistrationForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'contact', 'address', 'pincode', 'logo', 'owner_name', 'owner_contact']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email']  # You can adjust the fields as needed


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_shop = kwargs.pop('user_shop', None)  # Retrieve the shop of the current user
        super(ProductForm, self).__init__(*args, **kwargs)
        if user_shop:
            # Filter categories based on the shop of the current user
            self.fields['category'].queryset = Category.objects.filter(shop=user_shop)

    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']