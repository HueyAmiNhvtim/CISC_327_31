from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserData, ShoppingCart, Location, Order
from ..res_owner.models import Restaurant, Category, Food
from .forms import SearchForm, AddToCartForm


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
    if request.method != 'POST':
        # Blank form
        form = SearchForm()
    else:
        # POST request type confirmed; processing data
        form = SearchForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('search_results/')
    return render(request, 'user/search.html')


def search_results(request):
    """
    The page to view the restaurants near the user's location
    :param request: a Request object specific to Django
    """
    results = Restaurant.objects.order_by('location')
    context = {"results": results}
    return render(request, 'user/search_results.html', context)


def restaurant(request, restaurant_id: int):
    """
    The page to view a restaurant
    :param request: a Request object specific to Django
    :param restaurant_id: the id of the restaurant
    """
    categories = Category.objects.order_by('name')
    context = {"categories": categories}
    return render(request, 'user/restaurant.html', context)


def category(request, category_name: str):
    """
    The page to view the contents of a category
    :param request: a Request object specific to Django
    :param category_name: the name of the category
    """
    food_items = Food.objects.order_by('name')
    context = {"food_items": food_items}
    return render(request, 'user/category.html', context)


def food(request, food_name: str):
    """
    The page to view the details of a food item and add
    it to the user's cart
    :param request: a Request object specific to Django
    :param food_name: the name of the food item
    """
    if request.method != 'POST':
        # Blank form
        form = AddToCartForm()
    else:
        # POST request type confirmed; processing data
        form = AddToCartForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('shopping_cart/')
    food = Food.objects.order_by('name')
    context = {"food": food}
    return render(request, 'user/food.html', context)


def shopping_cart(request):
    """
    The page to view the user's shopping cart
    :param request: a Request object specific to Django
    """
    return render(request, 'user/shopping_cart.html')


def view_orders(request):
    """
    The page to view the user's orders
    :param request: a Request object specific to Django
    """
    orders = Order.objects.order_by('date_and_time')
    context = {"orders": orders}
    return render(request, 'user/view_orders.html', context)


def order(request):
    """
    The page to view details of an order
    :param request: a Request object specific to Django
    """
    return render(request, 'user/order.html')
