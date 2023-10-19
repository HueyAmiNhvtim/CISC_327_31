from django.shortcuts import render
from .models import RestaurantOwner, Restaurant, Food, Category
# Create your views here.


def res_home_page(request):
    """
    The home page for restaurant owners.
    Show all restaurants the owners own in alphabetical order
    :param request: a Request object specific to Django
    """
    restaurants = Restaurant.objects.order_by('name')
    # restaurants = Restaurant.objects.filter(owner=request.user).order_by('name')
    # For when user is working
    context = {"restaurants": restaurants}
    return render(request, 'res_owner/res_home_page.html', context)


def restaurant(request, restaurant_id: int):
    """
    The page for each restaurant.
    Show the menu
    :param request: a Request object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    foods = this_restaurant.food_set.all()
    # Find out how to get the categories through the restaurant's food...
    # Use Django shell for this shite.
    # Find all categories in all food of a restaurant.
    res_category = set()
    for food in foods:
        for category in food.category_set.all():
            res_category.add(category.name)
    sorted_category = sorted(list(res_category))
    print(sorted_category)
    context = {"categories": sorted_category}
    return render(request, 'res_owner/restaurant.html', context)
