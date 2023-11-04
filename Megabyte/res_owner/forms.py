from django import forms

from .models import Restaurant, Food, Category
from user.models import Order


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

    
class CategorizingForm(forms.ModelForm):
    """
    Form allows for assignment of food items within a restaurant to a chosen Category
    """
    # Potential Issue:
    # Since categories are shared among the restaurants. Multiple ChoiceField limits the amount of food specific
    # to that restaurant.... And it will only accidentally remove the food associating with the category from other
    # restaurants!
    def __init__(self, *args, **kwargs):
        self.restaurant_id = kwargs.pop('restaurant_id')
        super(CategorizingForm, self).__init__(*args, **kwargs)
        self.this_restaurant = Restaurant.objects.get(id=self.restaurant_id)
        self.fields['food'].queryset = Food.objects.filter(restaurant=self.this_restaurant)
        self.food_not_in_res = []
        # For getting food not in this restaurant but is associated with the category
        # This is to deal with that bug mentioned in Potential Issue
        if kwargs.get("instance"):
            self.existing_category = kwargs.pop('instance')
            for food in self.existing_category.food.all():
                if food.restaurant.name != self.this_restaurant.name:
                    self.food_not_in_res.append(food)

    class Meta:
        model = Category
        fields = ['name', 'food']
    name = forms.CharField(disabled=True)
    food = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
    )


class NewCategoryForm(forms.ModelForm):
    """
    Form allows for creation of new Category
    """
    def __init__(self, *args, **kwargs):
        self.restaurant_id = kwargs.pop('restaurant_id')
        super(NewCategoryForm, self).__init__(*args, **kwargs)
        self.this_restaurant = Restaurant.objects.get(id=self.restaurant_id)
        self.fields['food'].queryset = Food.objects.filter(restaurant=self.this_restaurant)
        self.food_not_in_res = []
        # For getting food not in this restaurant but is associated with the category
        if kwargs.get("instance"):
            self.existing_category = kwargs.pop('instance')
            for food in self.existing_category.food.all():
                if food.restaurant.name != self.this_restaurant.name:
                    self.food_not_in_res.append(food)

    class Meta:
        model = Category
        fields = ['name', 'food']

    name = forms.CharField()
    food = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


# WIP
# class ChangeOrderStatus(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['status']
#     pass
