from django.db import models


class UserData(models.Model):
    """A model representation of a user"""
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=128)

    def __str__(self):
        """Return the username of the user"""
        return self.username

    def change_username(self, new_username):
        """Change the user's username
        Params:
            new_username -> str: the user's new username
        Returns:
            True if the operation is successful
        """
        self.user_name = new_username
        return True

    def change_email(self, new_email):
        """Change the user's email
        Params:
            new_email -> str: the user's new email
        Returns:
            True if the operation is successful
        """
        self.email = new_email
        return True

    def change_password(self, new_password, verify_password):
        """Change the user's password
        Params:
            new_password -> str: the user's new password
            verify_password -> str: verification that the user typed 
                their new password correctly
        Returns:
            True if the operation is successful
            False if the new password and the verification do not match
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
        """Add a food item to cart
        Params:
            item -> str: name of the item to add
            restaurant -> str: name of restaurant
            quantity -> int: number of the item to add
            price -> float: price of a single unit of the item
        Returns:
            True if the operation is successful
            False if the item already exists in the shopping cart
                and the quantity is invalid
        """
        # Turn items into a list
        items_list = self.items.split(',')
        if item in items_list:
            # Item already exists in cart, add to quantity instead
            # Turn quantities into a list
            quantities_list = self.quantities.split(',')
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
        """Remove a food item from cart
        Params:
            item -> str: name of the food item to remove from the cart
        Returns:
            True if the food has been removed from the cart successfully
            False if the food did not exist in the cart
        """
        # Turn items into a list
        items_list = self.items.split(',')
        if item not in items_list:
            # Item to remove is not in list, operation failed
            return False
        else:
            # Turn other fields into lists
            restaurants_list = self.restaurants.split(',')
            quantities_list = self.quantities.split(',')
            prices_list = self.prices.split(',')
            # Find index of item to remove
            item_index = items_list.index(item)
            # Remove food
            items_list.pop(item_index)
            restaurants_list.pop(item_index)
            quantities_list.pop(item_index)
            prices_list.pop(item_index)
            self.items = ','.join(items_list)
            self.restaurants = ','.join(restaurants_list)
            self.quantities = ','.join(quantities_list)
            self.prices = ','.join(prices_list)
            # Operation successful
            return True

    def change_quantity(self, item: str, new_quantity: int):
        """Change the quantity of an existing item in the cart
        Params:
            item -> str: Food name
            new_quantity -> int: The new quantity of the food in the cart
        Returns:
            True if the operation is successful
            False if the quantity is below 0 or the item does not exist in the
                cart
        """
        if new_quantity < 0:
            # Quantity is below 0, operation failed
            return False
        else:
            # Turn items into a list
            items_list = self.items.split(',')
            if item not in items_list:
                # Item does not exist in shopping cart, operation failed
                return False
            else:
                # Turn quantities into a list
                quantities_list = self.quantities.split(',')
                # Find index of the item
                item_index = items_list.index(item)
                # Change quantity of the item to the new quantity
                quantities_list[item_index] = str(new_quantity)
                self.quantities = ','.join(quantities_list)
                # Operation successful
                return True
