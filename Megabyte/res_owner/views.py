from django.shortcuts import render
from .models import RestaurantOwner, Restaurant, Menu
# Create your views here.


def res_home_page(request):
    """
    The home page for restaurant owners.
    Show all restaurants the owners own in alphabetical order
    """
    restaurants = Restaurant.objects.order_by('name')
    # restaurants = Restaurant.objects.filter(owner=request.user).order_by('name')
    # For when user is working
    context = {"restaurants": restaurants}
    return render(request, 'res_owner/res_home_page.html', context)
