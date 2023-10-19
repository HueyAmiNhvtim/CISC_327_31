from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class RestaurantOwner(models.Model):
    """
    A model representation of a restaurant owner
    Will be deleted once user set up is done
    """
    # There is no way a person's name is that long
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=128)

    # For user...The User should be the Res_Owner_specific table one.
    associating_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return the name of the owner"""
        return self.name


class Restaurant(models.Model):
    """
    A model representation of a restaurant.
    Each owner can have multiple restaurants associating with it.
    """
    # I think I should associate user here rather than the res_owner.
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)  # May subject to change
    # Path to the image representation of the restaurant
    # Only change to FilePathField when you have the actual locations.
    # Else, it will result in errors. When changed, make sure to change
    # every other image_path of Restaurants created in admin page to valid file paths
    # as well.
    image_path = models.CharField(max_length=100)

    # This will have to be changed once custom User registrations are implemented
    # Delete blank and null once that happens
    restaurant_owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    # restaurant_owner = models.ForeignKey(RestaurantOwner, on_delete=models.CASCADE)

    def __str__(self):
        """Return the name of the restaurant"""
        return self.name


class Food(models.Model):
    """
    A model representation of a food item.
    A collection of food with a specific restaurant foreign key represents
    that restaurant's menu.
    """
    name = models.CharField(max_length=200)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        """Return the name of the food"""
        return self.name


class Category(models.Model):
    """
    A model representation of a food category
    A food item can have multiple categories.
    A category can have multiple food items associating with it.
    """
    # Allow existing owner to choose categories created by other owners through
    # a single database!
    name = models.CharField(max_length=200, primary_key=True)
    food = models.ManyToManyField(Food)
    # When restaurant_owner is going to assign category to food, the decision above makes sense

    class Meta:
        """Holds extra information for managing a model"""
        verbose_name_plural = "Categories"

    def __str__(self):
        """Return the name of the category"""
        return self.name

    def __eq__(self, other):
        """Return a boolean if objects have same name"""
        if type(other) != Category:
            return False
        return other.name == self.name

    def __hash__(self):
        """For equality comparison"""
        return hash(self.name)
