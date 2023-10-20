from django import forms

from .models import Restaurant, Food, Category

# If custom user.... import customer_user here or sth


class RestaurantForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the Restaurant model fields
        model = Restaurant
        # Fields you wish to be able to edit must match the fields variables in the corresponding
        # model!
        fields = ['name', 'location', 'image_path']


class FoodForm(forms.ModelForm):
    class Meta:
        # Tell Django to base this form off the Restaurant model fields
        model = Food
        # Fields you wish to be able to edit must match the fields variables in the corresponding
        # model!
        fields = ['name', 'price', 'image_path']


class CategoryForm(forms.ModelForm):
    nani = 0
