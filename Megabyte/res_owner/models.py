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
    """A model representation of a restaurant"""
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)  # May subject to change


