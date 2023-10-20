from django import forms

from .models import Location


class SearchForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the Location model fields
        model = Location
        # Fields you with to be able to edit must match the fields variables
        # in the corresponding model!
        fields = ['street', 'city', 'province_or_state',
                  'country', 'postal_code']
