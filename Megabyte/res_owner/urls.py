"""Define URL patterns for the res_owner sections"""
from django.urls import path
from . import views


app_name = 'res_owner'
urlpatterns = [
    # Home_page for restaurant owners
    path('', views.res_home_page, name='res_home_page'),
    # Page for each restaurant
    path('restaurants/<int:restaurant_id>/', views.restaurant, name='restaurant'),
    # Page for each category, the url patterns captures the arguments for the respective
    # views functions
    # ORDER MATTERS!! So for miscellaneous items. You have to put the path before the categorized ones
    path('categories/Others/<int:restaurant_id>', views.cat_others, name='cat_others'),
    path('categories/<category_name>/<int:restaurant_id>', views.category, name='category'),

]
