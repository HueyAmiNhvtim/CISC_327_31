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


class FoodFormDropDown(forms.ModelForm):
    # Forms that can have a dropdown list to choose the category, huh....
    class Meta:
        model = Food
        fields = ['name', 'price', 'image_path']


class CategoryForm(forms.ModelForm):
    nani = 0


class CategorizingForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'food']

    def __init__(self, *args, **kwargs):
        self.restaurant_id = kwargs.pop('restaurant_id')
        super(CategorizingForm, self).__init__(*args, **kwargs)
        name = forms.CharField()
        this_restaurant = Restaurant.objects.get(id=self.restaurant_id)
        food = forms.ModelChoiceField(
            queryset=Food.objects.filter(restaurant=this_restaurant),
            widget=forms.CheckboxSelectMultiple
        )

