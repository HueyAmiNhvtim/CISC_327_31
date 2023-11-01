from django.db import models


class UserData(models.Model):
    """A model representation of a user"""
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    cart = models.JSONField(default=list)

    def __str__(self):
        """Return the username of the user"""
        return self.username


class Quantity(models.Model):
    """A model representation of the amount of an item"""
    quantity = models.CharField(max_length=4)

    def __str__(self):
        """Return the quantity"""
        return self.quantity


class Location(models.Model):
    """Model representation of the user's location"""
    street = models.CharField(max_length=1024)
    city = models.CharField(max_length=256)
    province_or_state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        """Return the address of the user"""
        return self.street, self.city, self.province_or_state, self.country, self.postal_code


class Order(models.Model):
    """Model representation of an order"""
    status = models.TextChoices("status", "Sent Accepted Prepared Delivered")
    user = models.PositiveIntegerField()
    date_and_time = models.DateTimeField()
    cart = models.JSONField(default=list)

    def __str__(self):
        """Return the order id"""
        return str(self.date_and_time)
