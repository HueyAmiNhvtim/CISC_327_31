from django.shortcuts import render, redirect
from .models import RestaurantOwner, Restaurant, Food, Category
from .forms import RestaurantForm, FoodForm, CategoryForm, CategorizingForm
from django.http import Http404
# Create your views here.


def res_home_page(request):
    """
    The home page for restaurant owners.
    Show all restaurants the owners own in alphabetical order
    :param request: a Request object specific to Django
    :return: the rendering of the html page 'res_owner/res_home_page.html'
    """
    restaurants = Restaurant.objects.order_by('name')
    # restaurants = Restaurant.objects.filter(owner=request.user).order_by('name')
    # For when user is working
    context = {"restaurants": restaurants}
    return render(request, 'res_owner/res_home_page.html', context)


def restaurant(request, restaurant_id: int):
    """
    The page for each restaurant.
    Show all the categories of a restaurant
    :param request: a Request object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
    foods = this_restaurant.food_set.all()

    # Find all categories in all food of a restaurant.
    res_category = set()
    for food in foods:
        for food_category in food.category_set.all():
            res_category.add(food_category)
    sorted_category = sorted(list(res_category), key=lambda x: x.name)
    # Needs refactoring...also in the restaurant.html too
    context = {
        'categories': sorted_category,
        'restaurant': this_restaurant,
        'restaurant_name': this_restaurant.name,
        'restaurant_id': restaurant_id
    }
    return render(request, 'res_owner/restaurant.html', context)


def category(request, category_name: str, restaurant_id: int):
    """
    The page for each category.
    Show all foods associated with that category in the restaurant
    :param request: a Request object specific to Django
    :param category_name: the name of the category in the Category table
    :param restaurant_id: the id of the restaurant in the Restaurant table
    """
    this_category = Category.objects.get(name=category_name)
    foods = this_category.food.all()
    restaurant_name = foods[0].restaurant.name
    sorted_food = sorted(list(foods), key=lambda a: a.name)
    context = {
        'foods': sorted_food,
        'category_name': this_category.name,
        'restaurant_name': restaurant_name,
        'restaurant_id': restaurant_id
    }
    return render(request, 'res_owner/category.html', context)


def categorizing(request, category_name: str, restaurant_id: int):
    """
    The page for categorizing each category to the foods
    :param request: a Request object specific to Django
    :param category_name: the name of the category in the Category table
    :param restaurant_id: the id of the restaurant in the Restaurant table
    """
    this_category = Category.objects.get(name=category_name)

    if request.method != 'POST':
        # Initial request: Pre-fill form with the current entry
        form = CategorizingForm(restaurant_id=restaurant_id, instance=this_category)
    else:
        # POST request type confirmed, process data
        form = CategorizingForm(restaurant_id=restaurant_id, instance=this_category)
        # Might have to change it once custom form validation is implemented.
        if form.is_valid():
            form.save_m2m()
            return redirect('res_owner:res_home_page')

    # This sends the context to render the edit_restaurant.html
    context = {'form': form, 'category_name': category_name, 'restaurant_id': restaurant_id}
    return render(request, 'res_owner/categorizing.html', context)


def cat_others(request, restaurant_id: int):
    """
       The page for category Others
       Show all foods not categorized in the restaurant
       :param request: a Request object specific to Django
       :param restaurant_id: the id of the restaurant in the Restaurant table
   """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)
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


def res_settings(request):
    """
    The page for managing the restaurants
    :param request: a Request object specific to Django
    """
    restaurants = Restaurant.objects.order_by('name')
    # restaurants = Restaurant.objects.filter(owner=request.user).order_by('name')
    # For when user is working
    context = {
        'restaurants': restaurants
    }
    return render(request, 'res_owner/res_settings.html', context)


def new_restaurant(request):
    """
    The page for adding in a new restaurant.
    :param request: a Request object specific to Django
    """
    if request.method != 'POST':
        # Blank form
        form = RestaurantForm()
    else:
        # POST request type confirmed; processing data
        form = RestaurantForm(data=request.POST)
        # Might have to change it once custom form validation is implemented.
        if form.is_valid():
            new_restaurant = form.save(commit=False)
            # new_restaurant.restaurant_owner = request.owner
            new_restaurant.save()  # Save to the database
            return redirect('res_owner:res_home_page')
    context = {'form': form}
    return render(request, 'res_owner/new_restaurant.html', context)


def edit_restaurant(request, restaurant_id: int):
    """
    The page for editing an existing restaurant entry.
    :param request: a Request object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table
    """
    this_restaurant = Restaurant.objects.get(id=restaurant_id)

    # Uncomment when user registration is completed
    # if this_restaurant.restaurant_owner != request.user:
    #     raise Http404
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


def delete_restaurant(request, restaurant_id: int):
    """
    The page for deleting an existing restaurant entry.
    :param request: a Request object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table to delete
    """
    if request.method == 'POST':
        Restaurant.objects.filter(id=restaurant_id).delete()
    return redirect('res_owner:res_home_page')


def new_food(request, restaurant_id: int):
    """
    The page for adding in a new food without categories.
    :param request: a Request object specific to Django
    :param restaurant_id: the id of the restaurant in the Restaurant table
    """
    if request.method != 'POST':
        # Blank form
        form = FoodForm()
    else:
        this_restaurant = Restaurant.objects.get(id=restaurant_id)
        # POST request type confirmed; processing data
        form = FoodForm(data=request.POST)
        if form.is_valid():
            new_food = form.save(commit=False)
            new_food.restaurant = this_restaurant
            new_food.save()  # Save to the database
            return redirect('res_owner:res_home_page')
    context = {'form': form, 'restaurant_id': restaurant_id}
    return render(request, 'res_owner/new_food.html', context)


def edit_food(request, food_id: int):
    """
    The page for editing food info
    :param request: a Request object specific to Django
    :param food_id: the id of the food item in the food table
    """
    this_food = Food.objects.get(id=food_id)
    # Uncomment when user registration is completed
    # if this_food.restaurant.restaurant_owner != request.user:
    #     raise Http404
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
