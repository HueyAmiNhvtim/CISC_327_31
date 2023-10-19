from django.shortcuts import render
from .models import RestaurantOwner, Restaurant, Food
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

    return render(request, 'res_owner/restaurant.html')
