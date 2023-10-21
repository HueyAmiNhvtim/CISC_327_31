from django import forms

from .models import Location, UserData, Quantity
from res_owner.models import Food


class SearchForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the Location model fields
        model = Location
        # Fields you with to be able to edit must match the fields variables
        # in the corresponding model!
        fields = ['location']


class AddToCartForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the Food model fields
        model = Quantity
        # Fields you with to be able to edit must match the fields variables
        # in the corresponding model!
        fields = ['quantity']


class UserDataForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the Food model fields
        model = UserData
        # Fields you with to be able to edit must match the fields variables
        # in the corresponding model!
        fields = ['username', 'email', 'password']
