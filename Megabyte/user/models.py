from django.db import models


class UserData(models.Model):
    """A model representation of a user"""
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        """Return the username of the user"""
        return self.username

    def change_username(self, new_username: str):
        """
        Change the user's username
        :param new_username: the user's new username
        :return: True if the operation is successful
        """
        self.user_name = new_username
        return True

    def change_email(self, new_email):
        """
        Change the user's email
        :param new_email: the user's new email
        :return: True if the operation is successful
        """
        self.email = new_email
        return True

    def change_password(self, new_password, verify_password):
        """
        Change the user's password
        :param new_password: the user's new password
        :param verify_password: verification that the user typed their
            new password correctly
        :return: True if the operation is successful
        :return: False if the new password and the verification do not match
        """
        if verify_password == new_password:
            # Passwords match
            self.password = new_password
            return True
        else:
            # Passwords do not match
            return False


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

    def add(self, item: str, restaurant: str, quantity: int, price: float):
        """
        Add a food item to cart
        Params:
        :param item: name of the item to add
        :param restaurant: name of restaurant
        :param quantity: number of the item to add
        :param price: price of a single unit of the item
        :return: True if the operation is successful
        :return: False if the item already exists in the shopping cart 
            and the quantity is invalid
        """
        # Turn items into a list
        items_list = self.process(self.items)
        if item in items_list:
            # Item already exists in cart, add to quantity instead
            # Turn quantities into a list
            quantities_list = self.process(self.quantities)
            # Find index of the item
            item_index = items_list.index(item)
            # Find old quantity of the item
            old_quantity = int(quantities_list[item_index])
            # Add the quantity of the item that would have been added to cart
            #   to the old quantity of the item
            self.change_quantity(item, old_quantity + quantity)
        elif len(self.items) == 0:
            # Add new food to fields
            self.items += item
            self.restaurants += restaurant
            self.quantities += str(quantity)
            self.prices += str(price)
            # Operation successful
            return True
        else:
            # Add new food to fields
            self.items += ',' + item
            self.restaurants += ',' + restaurant
            self.quantities += ',' + str(quantity)
            self.prices += ',' + str(price)
            # Operation successful
            return True

    def remove(self, item: str):
        """
        Remove a food item from cart
        :param item: name of the food item to remove from the cart
        :return: True if the food has been removed from the cart successfully
        :return: False if the food did not exist in the cart
        """
        # Turn items into a list
        items_list = self.process(self.items)
        if item not in items_list:
            # Item to remove is not in list, operation failed
            return False
        else:
            # Turn other fields into lists
            restaurants_list = self.process(self.restaurants)
            quantities_list = self.process(self.quantities)
            prices_list = self.process(self.prices)
            # Find index of item to remove
            item_index = items_list.index(item)
            # Remove food
            items_list.pop(item_index)
            restaurants_list.pop(item_index)
            quantities_list.pop(item_index)
            prices_list.pop(item_index)
            self.items = self.convert(items_list)
            self.restaurants = self.convert(restaurants_list)
            self.quantities = self.convert(quantities_list)
            self.prices = self.convert(prices_list)
            # Operation successful
            return True

    def change_quantity(self, item: str, new_quantity: int):
        """
        Change the quantity of an existing item in the cart
        :param item: Food name
        :param new_quantity: The new quantity of the food in the cart
        :return: True if the operation is successful
        :return: False if the quantity is below 0 or the item does not 
            exist in the cart
        """
        if new_quantity < 0:
            # Quantity is below 0, operation failed
            return False
        else:
            # Turn items into a list
            items_list = self.process(self.items)
            if item not in items_list:
                # Item does not exist in shopping cart, operation failed
                return False
            else:
                # Turn quantities into a list
                quantities_list = self.process(self.quantities)
                # Find index of the item
                item_index = items_list.index(item)
                # Change quantity of the item to the new quantity
                quantities_list[item_index] = str(new_quantity)
                self.quantities = self.convert(quantities_list)
                # Operation successful
                return True

    def process(self, string_list):
        """
        Process a list in string form into a list
        :param string_list: a string to process
        :return: a list of strings
        """
        return string_list.split(',')

    def convert(self, list_of_strings):
        """
        Convert a list of strings to string form
        :param list_of_strings: a list of strings
        :return: the list in string form
        """
        return ','.join(list_of_strings)


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
