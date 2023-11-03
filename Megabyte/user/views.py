from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserData, Quantity, Location, Order
from res_owner.models import Restaurant, Category, Food
from .forms import UserDataForm, SearchForm, CartForm, OrderForm
import datetime


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
            return redirect('user:user_settings', user_id)
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
        form = CartForm()
    else:
        # POST request type confirmed; processing data
        form = CartForm(data=request.POST)
        if form.is_valid():
            new_cart = form.save(commit=False)
            new_cart.item = food_name
            new_cart.price = this_food_item.price
            new_cart.restaurant = this_restaurant
            new_cart.save()
            return redirect('shopping_cart/')
    context = {"form": form, "food": this_food_item,
               "restaurant": this_restaurant}
    return render(request, 'user/food.html', context)


def add_to_shopping_cart(request, user_id: int, restaurant_id: int, food_id: int):
    """
    Add food to a user's shopping cart
    :param request: a Request object specific to Django
    :param user_id: the id of the user
    :param restaurant_id: the id of the restaurant
    :param food_id: the id of the food item
    """
    this_user = UserData.objects.get(id=user_id)
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    this_food = Food.objects.get(id=food_id)

    if request.method != 'POST':
        # Blank form
        form = CartForm()
    else:
        # POST request type confirmed; processing data
        form = CartForm(data=request.POST)
        if form.is_valid():
            food_quantity = form.save(commit=False)
            food_in_cart = False
            for i in this_user.cart:
                # If the food item already exists in the cart,
                # add to the quantity of the item
                if i[4] == str(food_id):
                    i[3] = str(int(i[3]) + int(food_quantity.quantity))
                    food_in_cart = True
                    break
            if not food_in_cart:
                # If the food item is not in the cart already,
                # add it to the cart
                this_user.cart.append([this_food.name, this_restaurant.name,
                                       str(this_food.price),
                                       food_quantity.quantity, food_id])
            this_user.save()
            return redirect('user:shopping_cart', user_id)
    context = {"user": this_user,
               "range": range(len(this_user.cart["items"]))}
    return render(request, 'user/shopping_cart.html', context)


def shopping_cart(request, user_id: int):
    """
    The page to view the user's shopping cart
    :param request: a Request object specific to Django
    :param user_id: the id of the user
    """
    this_user = UserData.objects.get(id=user_id)
    context = {"user": this_user,
               "range": range(len(this_user.cart))}
    return render(request, 'user/shopping_cart.html', context)


def edit_quantity(request, user_id: int, food_id: int):
    """
    The page to change the amount of an item in a cart
    :param request: a Request object specific to Django
    :param user_id: the id of the user
    :param item: item whose quantity is to be changed
    """
    this_user = UserData.objects.get(id=user_id)
    this_food = Food.objects.get(id=food_id)
    if request.method != 'POST':
        # Initial request: Pre-fill form with the current entry
        form = CartForm()
    else:
        # POST request type confirmed, process data
        form = CartForm(data=request.POST)
        # Might have to change it once custom form validation is implemented.
        if form.is_valid():
            new_quantity = form.save(commit=False)
            for i in range(len(this_user.cart)):
                # Change the amount of the specified item
                if int(this_user.cart[i][4]) == food_id:
                    this_user.cart[i][3] = new_quantity.quantity
                    this_user.save()
                    break
            return redirect('user:shopping_cart', user_id)
    context = {"user": this_user, "food": this_food, "form": form}
    return render(request, 'user/edit_quantity.html', context)


def remove_food(request, user_id: int, food_id: int):
    this_user = UserData.objects.get(id=user_id)
    if request.method == 'POST':
        for i in range(len(this_user.cart)):
            # Change the amount of the specified item
            if int(this_user.cart[i][4]) == food_id:
                this_user.cart.pop(i)
                this_user.save()
                break
    return redirect('user:shopping_cart', user_id)


def checkout(request, user_id: int):
    this_user = UserData.objects.get(id=user_id)
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
        if form.is_valid():
            # Add info to Order model
            order_info = form.save(commit=False)
            order_info.status = "Sent"
            order_info.user = this_user.id
            order_info.date_and_time = datetime.datetime.now()
            order_info.cart = this_user.cart.copy()
            order_info.save()

            # Reset the user's shopping cart
            this_user.cart = []
            this_user.save()
        return redirect('user:view_orders', user_id)

    # This sends the context to render the view_orders.html
    context = {'form': form, 'user': this_user}
    return render(request, 'user/view_orders.html', context)


def view_orders(request, user_id: int):
    """
    The page to view the user's orders
    :param request: a Request object specific to Django
    :param user_id: the id of the user
    """
    this_user = UserData.objects.get(id=user_id)
    orders = Order.objects.filter(user=user_id)
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
