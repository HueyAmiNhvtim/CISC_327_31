from django.db import models


class UserData(models.Model):
    """A model representation of a user"""
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        """Return the username of the user"""
        return self.username


class ShoppingCart(models.Model):
    """A model representation of the shopping cart"""
    # 50000 is a placeholder, as max_length is required
    item = models.CharField(max_length=50000)
    restaurant = models.CharField(max_length=50000)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        default=0, decimal_places=2, max_digits=12)

    def __str__(self):
        """Return the item names"""
        return self.item


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
    user_id = models.PositiveIntegerField()
    date_and_time = models.DateTimeField()
    items = models.CharField(max_length=50000)
    restaurants = models.CharField(max_length=50000)
    quantities = models.CharField(max_length=50000)
    prices = models.CharField(max_length=50000)

    def __str__(self):
        """Return the order id"""
        return str(self.date_and_time)
