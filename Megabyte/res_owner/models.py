from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.


class Restaurant(models.Model):
    """
    A model representation of a restaurant.
    Each owner can have multiple restaurants associating with it.
    """
    # I think I should associate user here rather than the res_owner.
    name = models.CharField(max_length=200, unique=True)
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

    def __str__(self):
        """Return the name of the restaurant"""
        return self.name


class Food(models.Model):
    """
    A model representation of a food item.
    A collection of food with a specific restaurant foreign key represents
    that restaurant's menu. A restaurant can have multiple food items.
    """
    name = models.CharField(max_length=200)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, decimal_places=6, max_digits=12)
    image_path = models.CharField(default='', max_length=100)

    def __str__(self):
        """Return the name of the food"""
        return self.name


class Category(models.Model):
    """
    A model representation of a food category
    A food item can have multiple categories.
    A category can have multiple food items associating with it.
    And a food item can have multiple categories associated with it.
    """
    # Allow existing owner to choose categories created by other owners through
    # a single database!
    name = models.CharField(max_length=200, primary_key=True)
    food = models.ManyToManyField(Food)
    # When restaurant_owner is going to assign category to food, the decision above makes sense
    restaurant = models.ManyToManyField(Restaurant)

    class Meta:
        """Holds extra information for managing a model"""
        verbose_name_plural = "Categories"

    def __str__(self):
        """Return the name of the category"""
        return self.name

    def __hash__(self):
        """For equality comparison"""
        return hash(self.name)
