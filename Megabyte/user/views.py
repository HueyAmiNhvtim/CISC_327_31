from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserData, ShoppingCart, Location
from .forms import SearchForm


def user_home_page(request):
    """
    The home page for users.
    :param request: a Request object specific to Django
    """


def user_settings(request):
    """
    The page to manage user settings
    :param request: a Request object specific to Django
    """
    return HttpResponse("Settings")


def search(request):
    """
    The page to search for restaurants.
    :param request: a Request object specific to Django
    """
    if request.method != 'GET':
        # Blank form
        form = SearchForm()
    else:
        # POST request type confirmed; processing data
        form = SearchForm(data=request.GET)
        if form.is_valid():
            return redirect('restaurants/')
    return HttpResponse("Search")


def restaurant(request, restaurant_id: int):
    """
    The page to view a restaurant
    :param request: a Request object specific to Django
    :param restaurant_id: the id of the restaurant
    """


def shopping_cart(request, user_id: int):
    """
    The page to view the user's shopping cart
    :param request: a Request object specific to Django
    :param user_id: the id of the user
    """


def view_orders(request, user_id: int):
    """
    The page to view the user's orders
    :param request: a Request object specific to Django
    :param user_id: the id of the user
    """

    return HttpResponse("Order")


def order(request, order_id: int):
    """
    The page to view details of an order
    :param request: a Request object specific to Django
    :param order_id: the id of the order
    """
