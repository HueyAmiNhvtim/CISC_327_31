from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import *
from user.models import *
from res_owner.models import Restaurant, Food, Category

import datetime

'''
class TestUser(TestCase):
    def setUp(self):
        # Create accounts
        User = get_user_model()
        self.res_owner1 = User.objects.create_user(email='owner1@gmail.com',
                                                   username='Owner1', is_res_owner=True,
                                                   password="IAmAn0wner")
        self.res_owner2 = User.objects.create_user(email='owner2@gmail.com',
                                                   username='Owner2', is_res_owner=True,
                                                   password="IAmAn0wner")
        self.user = User.objects.create_user(email='user@gmail.com',
                                             username='user', is_res_owner=False,
                                             password="IAmAUs3r")
        # Create restuarants
        self.restaurant1 = Restaurant.objects.create(name="Fruit Market",
                                                    location="123 Main Street,City,Province,Country,123 ABC",
                                                    image_path="FruitMarket.png", restaurant_owner=self.res_owner1)
        self.restaurant2 = Restaurant.objects.create(name="Dollar Store",
                                                    location="124 Main Street,City,Province,Country,123 ABD",
                                                    image_path="DollarStore.png", restaurant_owner=self.res_owner1)
        self.restaurant3 = Restaurant.objects.create(name="Fruit Empire",
                                                    location="125 Main Street,City,Province,Country,123 ABE",
                                                    image_path="FruitEmpire.png", restaurant_owner=self.res_owner2)
        # Create Food items
        self.food1 = Food.objects.create(name="Apple", restaurant=self.restaurant1, price=1.00,
                                        image_path="Apple1.png")
        self.food2 = Food.objects.create(name="Banana", restaurant=self.restaurant1, price=1.79,
                                        image_path="Banana.png")
        self.food3 = Food.objects.create(name="Broccoli", restaurant=self.restaurant1, price=4.50,
                                        image_path="Broccoli.png")
        self.food4 = Food.objects.create(name="Loonie", restaurant=self.restaurant2, price=2.00,
                                        image_path="Loonie.png")
        self.food5 = Food.objects.create(name="Apple", restaurant=self.restaurant3, price=1.00,
                                        image_path="Apple2.png")
        # Create categories
        self.category1 = Category.objects.create(
            name="Fruits", food=[self.food1, self.food2])
        self.category2 = Category.objects.create(
            name="Veggies", food=[self.food3])
        self.category3 = Category.objects.create(
            name="Money", food=[self.food4])
        self.category4 = Category.objects.create(
            name="Fruits", food=[self.food5])

    def test_restaurant_navigation(self):
        pass
'''