"""Define URL patterns for the res_owner sections"""
from django.urls import path
from . import views

app_name = 'res_owner'
urlpatterns = [
    # Home_page for restaurant owners
    path('', views.res_home_page, name='res_home_page'),
    # Central page for adding/removing or editing restaurants
    path('restaurants_settings', views.res_settings, name='res_settings'),
    # Page for editing an existing restaurant entry
    path('edit_restaurant/<int:restaurant_id>', views.edit_restaurant, name='edit_restaurant'),
    # Page for adding in a new restaurant
    path('new_restaurant', views.new_restaurant, name='new_restaurant'),
    # Page for deleting the restaurant entry
    path('remove_restaurant/<int:restaurant_id>', views.delete_restaurant, name='delete_restaurant'),

    # Page for each restaurant
    path('restaurants/<int:restaurant_id>/', views.restaurant, name='restaurant'),
    # Page for each category, the url patterns captures the arguments for the respective
    # views functions
    # ORDER MATTERS!! So for miscellaneous items. You have to put the path before the categorized ones
    path('categories/Others/<int:restaurant_id>', views.cat_others, name='cat_others'),
    path('categories/<category_name>/<int:restaurant_id>', views.category, name='category'),

    # Page for categorizing food
    path('categorizing/<category_name>/<int:restaurant_id>', views.categorizing, name='categorizing'),
    # Page for adding in new categories
    path('new_category/<int:restaurant_id>', views.new_category, name='new_category'),

    # Page for adding in new food
    path('new_food/<int:restaurant_id>/', views.new_food, name='new_food'),
    # Page for editing food entries and categorizing them
    path('edit_food/<int:food_id>', views.edit_food, name='edit_food'),

]
