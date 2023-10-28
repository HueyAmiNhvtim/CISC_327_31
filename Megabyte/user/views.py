from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserData, ShoppingCart, Location, Order
from res_owner.models import Restaurant, Category, Food
from .forms import UserDataForm, SearchForm, AddToCartForm


def user_home_page(request):
    """
    The home page for users.
    :param request: a Request object specific to Django
    """
    return render(request, "user/user_home_page.html")


def user_settings(request, user_id: int):
    """
    The page to manage user settings
    :param request: a Request object specific to Django
    :param user_id: the id of the user
    """
    this_user = UserData.objects.get(id=user_id)
    if request.method != 'POST':
        # Initial request: Pre-fill form with the current entry
        form = UserDataForm(instance=this_user)
    else:
        # POST request type confirmed, process data
        form = UserDataForm(instance=this_user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('res_owner:user_settings')
    context = {'form': form, 'user': this_user}
    return render(request, "user/user_settings.html", context)


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
    context = {'form': form}
    return render(request, 'user/search.html', context)


def search_results(request):
    """
    The page to view the restaurants near the user's location
    :param request: a Request object specific to Django
    """

    restaurants = Restaurant.objects.order_by('location')
    context = {"restaurants": restaurants}
    return render(request, 'user/search_results.html', context)


def restaurant(request, restaurant_id: int):
    """
    The page to view a restaurant
    :param request: a Request object specific to Django
    :param restaurant_id: the id of the restaurant in the restaurant table
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    food_items = this_restaurant.food_set.all()
    # Find all categories in all food of a restaurant
    categories = set()
    for food in food_items:
        for category in food.category_set.all():
            categories.add(category)
    sorted_categories = sorted(list(categories), key=lambda x: x.name)
    context = {"restaurant": this_restaurant,
               "restaurant_id": restaurant_id,
               "categories": sorted_categories}
    return render(request, 'user/restaurant.html', context)


def category(request, restaurant_id: int, category_name: str):
    """
    The page to view the contents of a category
    :param request: a Request object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table
    :param category_name: the name of the category
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    this_category = Category.objects.get(name=category_name)
    all_food_items = this_category.food.all()
    food_items = []
    for food in all_food_items:
        if food.restaurant.name == this_restaurant.name:
            food_items.append(food)
    restaurant_name = food_items[0].restaurant.name
    sorted_food_items = sorted(food_items, key=lambda x: x.name)
    context = {"restaurant_id": restaurant_id,
               "restaurant_name": restaurant_name,
               "category_name": category_name,
               "food_items": sorted_food_items}
    return render(request, 'user/category.html', context)


def food(request, restaurant_id: int, category_name: str, food_name: str):
    """
    The page to view the details of a food item and add
    it to the user's cart
    :param request: a Request object specific to Django
    :param food_name: the name of the food item
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    this_food_item = Food.objects.get(
        restaurant=this_restaurant, name=food_name)
    if request.method != 'POST':
        # Blank form
        form = AddToCartForm()
    else:
        # POST request type confirmed; processing data
        form = AddToCartForm(data=request.POST)
        if form.is_valid():
            new_cart = form.save(commit=False)
            new_cart.item = food_name
            new_cart.price = this_food_item.price
            new_cart.restaurant = restaurant_id
            new_cart.save()
            return redirect('shopping_cart/')
    context = {"form": form}
    return render(request, 'user/food.html', context)


def shopping_cart(request):
    """
    The page to view the user's shopping cart
    :param request: a Request object specific to Django
    """
    cart = ShoppingCart.objects.order_by('item')
    context = {"cart": cart}
    return render(request, 'user/shopping_cart.html')


def view_orders(request, user_id: int):
    """
    The page to view the user's orders
    :param request: a Request object specific to Django
    :param user_id: the id of the user
    """
    this_user = UserData.objects.get(id=user_id)
    orders = Order.objects.order_by('date_and_time')
    context = {"user": this_user, "orders": orders}
    return render(request, 'user/view_orders.html', context)


def order(request, user_id: int, order_id: int):
    """
    The page to view details of an order
    :param request: a Request object specific to Django
    :param order_id: the id of the order
    :param user_id: the id of the user
    """
    this_user = UserData.objects.get(id=user_id)
    this_order = Order.objects.get(id=order_id)
    context = {"user": this_user, "order": this_order}
    return render(request, 'user/order.html', context)
