from django import forms

from .models import Location, UserData, ShoppingCart
from res_owner.models import Food


class SearchForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the Location model fields
        model = Location
        # Fields you with to be able to edit must match the fields variables
        # in the corresponding model!
        fields = ['street', 'city', 'province_or_state',
                  'country', 'postal_code']


class CartForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the Food model fields
        model = ShoppingCart
        # Fields you with to be able to edit must match the fields variables
        # in the corresponding model!
        fields = ['quantities']


class UserDataForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the UserData model fields
        model = UserData
        # Fields you with to be able to edit must match the fields variables
        # in the corresponding model!
        fields = ['username', 'email', 'password']
