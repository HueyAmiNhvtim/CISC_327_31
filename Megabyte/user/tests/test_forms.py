from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import *
from user.forms import *
from res_owner.models import Restaurant, Food


class TestSearchForm(TestCase):
    def setUp(self):
        User = get_user_model()
        self.client = Client()
        # Create a restaurant owner and a restaurant to search for
        self.res_owner1 = User.objects.create_user(email='owner1@gmail.com',
                                                   username='Owner1', is_res_owner=True,
                                                   password="IAmAn0wner")
        self.restaurant1 = Restaurant.objects.create(name="Fruit Market",
                                                    location="123 Main Street,City,Province,Country,123 ABC",
                                                    image_path="FruitMarket.png", restaurant_owner=self.res_owner1)
        # Create a user
        self.user = User.objects.create_user(email='user@gmail.com',
                                             username='user', is_res_owner=False,
                                             password="IAmAUs3r")
        # Navigate to search page
        self.client.login(email="user@gmail.com",password="IAmAUs3r")
        self.search_view_func = reverse(viewname='user:search')

    def test_SearchForm_valid_data(self):
        """Test if SearchForm accepts the specified valid data"""
        form = SearchForm(data={"street": "21-25 Union Street",
                                "city": "Kingston",
                                "province_or_state": "Ontario",
                                "country": "Canada",
                                "postal_code": "K7L 2N8"})
        self.assertTrue(form.is_valid(), "SearchForm for valid data is invalid")

    def test_SearchForm_invalid_data(self):
        """Test if SearchForm does not accept the specified invalid data"""
        form = SearchForm(data={"street": "21-25 Union Street",
                                "city": "Kingston",
                                "province_or_state": "Ontario",
                                "postal_code": "K7L 2N8"})
        self.assertFalse(form.is_valid(), "SearchForm for invalid data is valid")

class TestCartForm(TestCase):
    def setUp(self):
        User = get_user_model()
        self.client = Client()
        # Create a restaurant owner and a restaurant to search for
        self.res_owner1 = User.objects.create_user(email='owner1@gmail.com',
                                                   username='Owner1', is_res_owner=True,
                                                   password="IAmAn0wner")
        self.restaurant1 = Restaurant.objects.create(name="Fruit Market",
                                                    location="123 Main Street,City,Province,Country,123 ABC",
                                                    image_path="FruitMarket.png", restaurant_owner=self.res_owner1)
        self.food1 = Food.objects.create(name="Apple", restaurant=self.restaurant1, price=1.00,
                                        image_path="Apple1.png")
        # Create a user
        self.user = User.objects.create_user(email='user@gmail.com',
                                             username='user', is_res_owner=False,
                                             password="IAmAUs3r")
        # Navigate to edit_quantity page
        self.client.login(email="user@gmail.com",password="IAmAUs3r")
        self.edit_quantity_view_func = reverse(viewname='user:edit_quantity', args=[self.food1.id])

    def test_CartForm_valid_data(self):
        """Test if CartForm accepts the specified valid data"""
        form = CartForm(data={"quantity": 5})
        self.assertTrue(form.is_valid(), "CartForm for valid data is invalid")

    def test_CartForm_invalid_data(self):
        """Test if CartForm does not accept the specified invalid data"""
        form = CartForm(data={})
        self.assertFalse(form.is_valid(), "CartForm for invalid data is valid")



class TestOrderForm(TestCase):
    def setUp(self):
        User = get_user_model()
        self.client = Client()
        # Create a restaurant owner and a restaurant to search for
        self.res_owner1 = User.objects.create_user(email='owner1@gmail.com',
                                                   username='Owner1', is_res_owner=True,
                                                   password="IAmAn0wner")
        self.restaurant1 = Restaurant.objects.create(name="Fruit Market",
                                                    location="123 Main Street,City,Province,Country,123 ABC",
                                                    image_path="FruitMarket.png", restaurant_owner=self.res_owner1)
        # Create a user
        self.user = User.objects.create_user(email='user@gmail.com',
                                             username='user', is_res_owner=False,
                                             password="IAmAUs3r")
        # Navigate to checkout page
        self.client.login(email="user@gmail.com",password="IAmAUs3r")
        self.checkout_view_func = reverse(viewname='user:checkout')

    def test_OrderForm_valid_data(self):
        """Test if OrderForm accepts the specified valid data"""
        form = OrderForm(data={})
        self.assertTrue(form.is_valid(), "OrderForm for valid data is invalid")