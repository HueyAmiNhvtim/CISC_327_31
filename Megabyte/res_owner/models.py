from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class RestaurantOwner(models.Model):
    """A model representation of a restaurant owner"""
    # There is no way a person's name is that long
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=128)

    # For user...
    associating_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return the name of the owner"""
        return self.name


class Restaurant(models.Model):
    """
    A model representation of a restaurant.
    Each owner can have multiple restaurants associating with it.
    """
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)  # May subject to change
    # Path to the image representation of the restaurant
    image_path = models.CharField(max_length=200)

    restaurant_owner = models.ForeignKey(RestaurantOwner, on_delete=models.CASCADE)

    def __str__(self):
        """Return the name of the restaurant"""
        return self.name


class Menu(models.Model):
    """
    A model representation of a menu.
    Each restaurant has a menu table associating with it.
    """
    food = models.CharField(max_length=200)
    # a food item can have multiple categories, hence the extended max_length to
    # contain the concatenated string of categories
    categories = models.CharField(max_length=500)

    restaurant_owning_menu = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


