from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserData, ShoppingCart, Location, Order
from .forms import SearchForm


def user_home_page(request):
    """
    The home page for users.
    :param request: a Request object specific to Django
    """
    return render(request, "user/user_home_page.html")


def user_settings(request):
    """
    The page to manage user settings
    :param request: a Request object specific to Django
    """
    return render(request, "user/user_settings.html")


def search(request):
    """
    The page to search for restaurants.
    :param request: a Request object specific to Django
    """
    if request.method != 'GET':
        # Blank form
        form = SearchForm()
    else:
        # GET request type confirmed; processing data
        form = SearchForm(data=request.GET)
        if form.is_valid():
            form.save()
            return redirect('restaurants/')
    return render(request, 'user/search.html')


def restaurant(request, restaurant_id: int):
    """
    The page to view a restaurant
    :param request: a Request object specific to Django
    :param restaurant_id: the id of the restaurant
    """
    return render(request, 'user/restaurant.html')


def shopping_cart(request, user_id: int):
    """
    The page to view the user's shopping cart
    :param request: a Request object specific to Django
    :param user_id: the id of the user
    """
    return render(request, 'user/shopping_cart.html')


def view_orders(request):
    """
    The page to view the user's orders
    :param request: a Request object specific to Django
    :param user_id: the id of the user
    """
    orders = Order.objects.order_by('date_and_time')
    context = {"orders": orders}
    return render(request, 'user/view_orders.html', context)


def order(request, order_id: int):
    """
    The page to view details of an order
    :param request: a Request object specific to Django
    :param order_id: the id of the order
    """
    return render(request, 'user/order.html')
