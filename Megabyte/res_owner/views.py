from django.shortcuts import render, redirect
from .models import Restaurant, Food, Category
from .forms import RestaurantForm, FoodForm, CategorizingForm, NewCategoryForm

from accounts.models import CustomUser
from user.models import Order

from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.


@login_required
def res_home_page(request):
    """
    The home page for the restaurant owner
    Show all the categories of a restaurant
    :param request: a HttpRequest object specific to Django
    :return the rendering of the html page 'res_owner/res_home_page.html'
    """
    this_user = CustomUser.objects.get(id=request.user.id)
    # Make sure non-res-owners can't get access to the restaurant owner page
    if not this_user.is_res_owner:
        raise Http404
    restaurants = this_user.restaurant_set.all()
    context = {'restaurants': restaurants}
    return render(request, 'res_owner/res_home_page.html', context)


@login_required
def restaurant(request, restaurant_id: int):
    """
    The page for each restaurant.
    Show all the categories of a restaurant
    :param request: a HttpRequest object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table
    :return the rendering of the html page 'res_owner/restaurant.html'
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    # Check to make sure different user cannot enter into other users' pages
    if this_restaurant.restaurant_owner != request.user:
        raise Http404
    res_category = this_restaurant.category_set.all()
    sorted_category = sorted(list(res_category), key=lambda x: x.name)
    # Needs refactoring...also in the restaurant.html too
    context = {
        'categories': sorted_category,
        'restaurant': this_restaurant,
        'restaurant_name': this_restaurant.name,
        'restaurant_id': restaurant_id
    }
    return render(request, 'res_owner/restaurant.html', context)


@login_required
def category(request, category_name: str, restaurant_id: int):
    """
    The page for each category.
    Show all foods associated with that category in the restaurant.
    :param request: a HttpRequest object specific to Django
    :param category_name: the name of the category in the Category table
    :param restaurant_id: the id of the restaurant in the Restaurant table
    :return the rendering of the html page 'res_owner/category.html'
    """
    this_category = Category.objects.get(name=category_name)
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    # Check to make sure different user cannot enter into other users' pages
    if this_restaurant.restaurant_owner != request.user:
        raise Http404
    all_foods = this_category.food.all()
    foods = []
    for food in all_foods:
        if food.restaurant.name == this_restaurant.name:
            foods.append(food)
    restaurant_name = this_restaurant.name
    sorted_food = sorted(foods, key=lambda a: a.name)
    context = {
        'foods': sorted_food,
        'category_name': this_category.name,
        'restaurant_name': restaurant_name,
        'restaurant_id': restaurant_id
    }
    return render(request, 'res_owner/category.html', context)


@login_required
def categorizing(request, category_name: str, restaurant_id: int):
    """
    The page for assigning a category to the foods
    :param request: a HttpRequest object specific to Django
    :param category_name: the name of the category in the Category table
    :param restaurant_id: the id of the restaurant in the Restaurant table
    :return the rendering of the html page 'res_owner/categorizing.html' upon a GET request
            or a redirect to the home page upon a successful POST request
    """
    this_category = Category.objects.get(name=category_name)
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    # Check to make sure different user cannot enter into other users' pages
    if this_restaurant.restaurant_owner != request.user:
        raise Http404
    if request.method != 'POST':
        # Initial request: Pre-fill form with the current entry
        form = CategorizingForm(
            restaurant_id=restaurant_id, instance=this_category)
    else:
        # POST request type confirmed, process data
        form = CategorizingForm(
            data=request.POST, restaurant_id=restaurant_id, instance=this_category)
        if form.is_valid():
            form.save()
            if len(form.food_not_in_res) > 0:
                existing_cat_name = form.data['name']
                this_category = Category.objects.get(name=existing_cat_name)
                for food in form.food_not_in_res:
                    this_category.food.add(food)
                this_category.save()
            return redirect('res_owner:res_home_page')

    # This sends the context to render the edit_restaurant.html
    context = {'form': form, 'category_name': category_name,
               'restaurant_id': restaurant_id}
    return render(request, 'res_owner/categorizing.html', context)


@login_required
def new_category(request, restaurant_id: int):
    """
    The page for adding new categories + categorization of food items.
    :param request: a HttpRequest object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table
    :return the rendering of the html page 'res_owner/new_category.html' upon a GET request
            or a redirect to the home page upon a successful POST request
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    # Check to make sure different user cannot enter into other users' pages
    if this_restaurant.restaurant_owner != request.user:
        raise Http404
    if request.method != 'POST':
        # Empty Form
        form = NewCategoryForm(restaurant_id=restaurant_id)
    else:
        # POST request type confirmed, process data
        form = NewCategoryForm(data=request.POST, restaurant_id=restaurant_id)

        # Check if there is an error associated with field name in the form. Cursed, I know.
        if form.errors.get('name') is not None:
            # When the duplicate key in Category table exists.
            if form.errors['name'].as_data():
                existing_cat_name = form.data['name']
                this_category = Category.objects.get(name=existing_cat_name)
                form = NewCategoryForm(
                    data=request.POST,
                    restaurant_id=restaurant_id,
                    instance=this_category
                )
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.restaurant.add(this_restaurant)
            new_category.save()
            if len(form.food_not_in_res) > 0:
                existing_cat_name = form.data['name']
                this_category = Category.objects.get(name=existing_cat_name)
                # Readd food from other restaurants to the Category.
                # This is due to the MultipleChoiceField in NewCategory form that can cause foods from other restaurants
                # to be uncategorized when only foods from this restaurant that can be categorized appears in that field
                for food in form.food_not_in_res:
                    this_category.food.add(food)
                this_category.save()
            return redirect('res_owner:res_home_page')

    # This sends the context to render the edit_restaurant.html
    context = {'form': form, 'restaurant_id': restaurant_id}
    return render(request, 'res_owner/new_category.html', context)


@login_required
def delete_category(request, category_name: str, restaurant_id: int):
    """
    The view function that handles the deletion of a category off a restaurant.
    If the category still has data assigned to it, then simply remove the category off
    every food in this restaurant. If not, then just delete it off the database.
    :param request: a HttpRequest object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table
    :param category_name: the name of the category in the Category table
    :return a redirect to the home page upon a successful POST request
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    # Check to make sure different user cannot enter into other users' pages
    if this_restaurant.restaurant_owner != request.user:
        raise Http404

    if request.method == 'POST':
        this_category = Category.objects.get(name=category_name)
        foods = this_restaurant.food_set.all()
        # Count the number of foods in this restaurant with this category
        foods_with_same_cat = 0
        for food in foods:
            for food_category in food.category_set.all():
                # Remove every food associated with this category in this restaurant when deleting the category
                if food_category.name == category_name:
                    this_category.food.remove(food)
                    foods_with_same_cat += 1
        # Remove the restaurant associating with this category too
        this_category.restaurant.remove(this_restaurant)
        # print(this_category.food.all())
        # print(foods_with_same_cat)
        # Basically, this means this category is used only by this restaurant. So delete it off the database also
        # if foods_with_same_cat == this_category.food.count():
        #     Category.objects.filter(name=category_name).delete() # DOES NOT WORK FOR NOW...
    return redirect('res_owner:res_home_page')


@login_required
def cat_others(request, restaurant_id: int):
    """
       The page for category Others
       Show all foods not categorized in the restaurant
       :param request: a HttpRequest object specific to Django
       :param restaurant_id: the id of the restaurant in the Restaurant table
       :return the rendering of the HTML page 'res_owner/category.html'
   """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    # Check to make sure different user cannot enter into other users' pages
    if this_restaurant.restaurant_owner != request.user:
        raise Http404
    all_foods = this_restaurant.food_set.all()
    no_category = []
    for food in all_foods:
        # Only add in food items that are not categorized
        if len(food.category_set.all()) == 0:
            no_category.append(food)
    sorted_food = sorted(list(no_category), key=lambda a: a.name)
    context = {
        'foods': sorted_food,
        'category_name': 'Others',
        'restaurant_name': this_restaurant.name,
        'restaurant_id': restaurant_id
    }
    return render(request, 'res_owner/category.html', context)


@login_required
def res_settings(request):
    """
    The page for managing the restaurants
    :param request: a HttpRequest object specific to Django
    :return the rendering of the HTML page 'res_owner/res_settings.html'
    """
    # Disallow non restaurant owners from accessing restaurant-owner specific pages
    if request.user.is_res_owner is False:
        raise Http404
    restaurants = Restaurant.objects.filter(restaurant_owner=request.user).order_by('name')
    context = {
        'restaurants': restaurants
    }
    return render(request, 'res_owner/res_settings.html', context)


@login_required
def new_restaurant(request):
    """
    The page for adding in a new restaurant.
    :param request: a HttpRequest object specific to Django
    :return the rendering of the HTML page 'res_owner/new_restaurant.html' upon a GET request
            or a redirect to the home page upon a successful POST request
    """
    # Disallow non restaurant owners from accessing restaurant-owner specific pages
    if request.user.is_res_owner is False:
        raise Http404

    if request.method != 'POST':
        # Blank form
        form = RestaurantForm()
    else:
        # POST request type confirmed; processing data
        form = RestaurantForm(data=request.POST)
        # Might have to change it once custom form validation is implemented.
        if form.is_valid():
            new_restaurant = form.save(commit=False)
            new_restaurant.restaurant_owner = request.user
            new_restaurant.save()  # Save to the database
            return redirect('res_owner:res_home_page')
    context = {'form': form}
    return render(request, 'res_owner/new_restaurant.html', context)


@login_required
def edit_restaurant(request, restaurant_id: int):
    """
    The page for editing an existing restaurant entry.
    :param request: a HttpRequest object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table
    :return The rendering of the HTML page 'res_owner/edit_restaurant.html' upon a GET request
            or a redirect to the home page upon a successful POST request.
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    # Check to make sure different user cannot enter into other users' pages
    if this_restaurant.restaurant_owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request: Pre-fill form with the current entry
        form = RestaurantForm(instance=this_restaurant)
    else:
        # POST request type confirmed, process data
        form = RestaurantForm(instance=this_restaurant, data=request.POST)
        # Might have to change it once custom form validation is implemented.
        if form.is_valid():
            form.save()
            return redirect('res_owner:res_home_page')
    # This sends the context to render the edit_restaurant.html
    context = {'form': form, 'restaurant': this_restaurant}
    return render(request, 'res_owner/edit_restaurant.html', context)


@login_required
def delete_restaurant(request, restaurant_id: int):
    """
    The view function that handles the deletion of a restaurant
    :param request: a HttpRequest object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table to delete
    :return A redirect to the home page upon a successful POST request.
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    # Check to make sure different user cannot enter into other users' pages
    if this_restaurant.restaurant_owner != request.user:
        raise Http404
    if request.method == 'POST':
        Restaurant.objects.filter(id=restaurant_id).delete()
    return redirect('res_owner:res_home_page')


@login_required
def new_food(request, restaurant_id: int):
    """
    The page for adding in a new food without categories.
    :param request: a HttpRequest object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table
    :return The rendering of the HTML page 'res_owner/new_food.html' upon a GET request
            or a redirect to the home page upon a successful POST request.
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    # Check to make sure different user cannot enter into other users' pages
    if this_restaurant.restaurant_owner != request.user:
        raise Http404
    if request.method != 'POST':
        # Blank form
        form = FoodForm()
    else:
        this_restaurant = Restaurant.objects.get(id=restaurant_id)
        # POST request type confirmed; processing data
        form = FoodForm(data=request.POST)
        if form.is_valid() and not this_restaurant.food_set.filter(name=request.POST.get('name')):
            new_food = form.save(commit=False)
            new_food.restaurant = this_restaurant
            new_food.save()  # Save to the database
            return redirect('res_owner:res_home_page')
    context = {'form': form, 'restaurant_id': restaurant_id}
    return render(request, 'res_owner/new_food.html', context)


@login_required
def edit_food(request, food_id: int):
    """
    The page for editing food info
    :param request: a HttpRequest object specific to Django
    :param food_id: the id of the food item in the Food table
    :return The rendering of the HTML page 'res_owner/edit_food.html' upon a GET request
            or a redirect to the home page upon a successful POST request.
    """
    this_food = Food.objects.get(id=food_id)
    # Check to make sure different user cannot enter into other users' pages
    if this_food.restaurant.restaurant_owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request: Pre-fill form with the current entry
        form = FoodForm(instance=this_food)
    else:
        # POST request type confirmed, process data
        form = FoodForm(instance=this_food, data=request.POST)
        # Might have to change it once custom form validation is implemented.
        if form.is_valid():
            form.save()
            return redirect('res_owner:res_home_page')
    # This sends the context to render the edit_restaurant.html
    context = {'form': form, 'food': this_food}
    return render(request, 'res_owner/edit_food.html', context)


@login_required
def delete_food(request, food_id: int):
    """
    The page for deleting an existing restaurant entry.
    :param request: a HttpRequest object specific to Django
    :param food_id: the id of the food in the Food table to delete
    :return A redirect to the home page upon a successful POST request
    """
    this_food = Food.objects.get(id=food_id)
    this_restaurant = this_food.restaurant
    # Check to make sure different user cannot enter into other users' pages
    if this_food.restaurant.restaurant_owner != request.user:
        raise Http404

    if request.method == 'POST':
        Food.objects.filter(id=food_id).delete()
    return redirect('res_owner:restaurant', restaurant_id=this_restaurant.id)


# This might be a bad one....
# This require order to have a foreign key to the restaurant.
@login_required
def order_management(request):
    """
    The page for viewing the list of orders for a restaurant.
    :param request: a HttpRequest object specific to Django
    :return the rendering of the HTML page orders.html
    """
    # Prevent normal user from accessing the restaurant owner pages
    # Allowing res_owner to delete past order is QOL really....
    if request.user.is_res_owner is False:
        raise Http404
    all_restaurants = request.user.restaurant_set.all()
    orders = []
    for a_restaurant in all_restaurants:
        orders.append(list(a_restaurant.order_set.all()))
    context = {'orders': orders}
    return render(request, 'res_owner/orders.html', context)


# WIP
@login_required
def change_order_status(request, order_id):
    """
    The page for changing the status of the order.
    :param request: a HttpRequest object specific to Django
    :param order_id: the id of the order in the Order table
    """
    this_order = Order.objects.get(id=order_id)
    # Allow only the owner of this order's restaurant to see the order
    if this_order.restaurants.restaurant_owner != request.user:
        raise Http404
    if request.method != 'POST':
        pass
    else:
        pass
    # The form should be similar to the radio button except you can only choose one.
    available_statuses = ["Waiting", "Rejected", "Accepted", "Delivered"]
    context = {'availabe_statuses': available_statuses}
    return render(request, 'res_owner/change_order_status.html', context)
