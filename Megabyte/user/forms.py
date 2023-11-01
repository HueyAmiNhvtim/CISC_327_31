from django import forms

from .models import Location, UserData, Quantity, Order


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
        model = Quantity
        # Fields you wish to be able to edit must match the fields variables
        # in the corresponding model!
        fields = ['quantity']


class UserDataForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the UserData model fields
        model = UserData
        # Fields you wish to be able to edit must match the fields variables
        # in the corresponding model!
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class OrderForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the Order model fields
        model = Order
        # Fields you wish to be able to edit must match the fields variables
        # in the corresponding model!
        fields = []
