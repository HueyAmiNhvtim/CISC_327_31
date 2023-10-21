from django.db import models


class UserData(models.Model):
    """A model representation of a user"""
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        """Return the username of the user"""
        return self.username


class Quantity(models.Model):
    """
    A model representation of the quantity field to add
    multiple of a type of a food item to a cart
    """
    quantity = models.PositiveIntegerField()

    def __str__(self):
        """Return the quantity of the item"""
        return str(self.quantity)


class ShoppingCart(models.Model):
    """A model representation of the shopping cart"""
    # 50000 is a placeholder, as max_length is required
    items = models.CharField(max_length=50000)
    restaurants = models.CharField(max_length=50000)
    quantities = models.CharField(max_length=50000)
    prices = models.CharField(max_length=50000)

    def __str__(self):
        """Return the item names"""
        return self.items


class Location(models.Model):
    """Model representation of the user's location"""
    location = models.CharField(max_length=1024)

    def __str__(self):
        """Return the address of the user"""
        return self.location


class Order(models.Model):
    """Model representation of an order"""
    order_id = models.PositiveIntegerField()
    date_and_time = models.DateTimeField()
    items = models.CharField(max_length=50000)
    restaurants = models.CharField(max_length=50000)
    quantities = models.CharField(max_length=50000)
    prices = models.CharField(max_length=50000)

    def __str__(self):
        """Return the order id"""
        return str(self.order_id)
