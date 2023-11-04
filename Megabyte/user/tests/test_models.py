from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import *
from user.models import *
from res_owner.models import Restaurant, Food

import datetime


class TestQuantityModel(TestCase):
    def setUp(self):
        self.quantity = Quantity.objects.create(quantity=2)

    def test_get_fields(self):
        """
        Check that the model has the specified fields
        """
        raised = False
        try:
            self.quantity._meta.get_field('quantity')
        except FieldDoesNotExist:
            raised = True
        self.assertFalse(raised, 'One or more fields do not exist')

    def test_max_length_of_fields(self):
        """
        Check to make sure all fields' max lengths values of this model
        are expected to equal specific numbers
        """
        max_quantity_length = self.quantity._meta.get_field('quantity').max_length
        self.assertEqual(max_quantity_length, 4,
                         'Invalid maximum length of quality field')


class TestLocationModel(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            street="21-25 Union Street", city="Kingston",
            province_or_state="Ontario", country="Canada",
            postal_code="K7L 2N8"
        )

    def test_get_fields(self):
        """
        Check that the model has the specified fields
        """
        raised = False
        try:
            self.location._meta.get_field('street')
            self.location._meta.get_field('city')
            self.location._meta.get_field('province_or_state')
            self.location._meta.get_field('country')
            self.location._meta.get_field('postal_code')
        except FieldDoesNotExist:
            raised = True
        self.assertFalse(raised, 'One or more fields do not exist')

    def test_max_length_of_fields(self):
        """
        Check to make sure all fields' max lengths values of this model
        are expected to equal specific numbers
        """
        # Retrieve maximum length of fields
        max_street_length = self.location._meta.get_field('street').max_length
        max_city_length = self.location._meta.get_field('city').max_length
        max_province_or_state_length = self.location._meta.get_field(
            'province_or_state').max_length
        max_country_length = self.location._meta.get_field('country').max_length
        max_postal_code_length = self.location._meta.get_field('postal_code').max_length

        # Test field lengths
        self.assertEqual(max_street_length, 1024,
                         'Invalid maximum length of street field')
        self.assertEqual(max_city_length, 256,
                         'Invalid maximum length of city field')
        self.assertEqual(max_province_or_state_length, 100,
                         'Invalid maximum length of province_or_state field')
        self.assertEqual(max_country_length, 100,
                         'Invalid maximum length of country field')
        self.assertEqual(max_postal_code_length, 10,
                         'Invalid maximum length of postal_code field')


class TestOrderModel(TestCase):
    def setUp(self):
        # Create accounts
        User = get_user_model()
        self.res_owner1 = User.objects.create_user(email='owner1@gmail.com',
                                                   username='Owner1', is_res_owner=True,
                                                   password="IAmAn0wner")
        self.user = User.objects.create_user(email='user@gmail.com',
                                             username='user', is_res_owner=False,
                                             password="IAmAUs3r")

        # Create restuarants
        self.restaurant1 = Restaurant.objects.create(name="Fruit Market",
                                                    location="123 Main Street,City,Province,Country,123 ABC",
                                                    image_path="FruitMarket.png", restaurant_owner=self.res_owner1)

        # Create Food items
        self.food1 = Food.objects.create(name="Apple", restaurant=self.restaurant1, price=1.00,
                                        image_path="Apple1.png")

        self.order = Order.objects.create(
            status="2", user=self.user.id, date_and_time=datetime.datetime.now(),
            cart=[[self.food1.name, self.restaurant1.name,
                   str(self.food1.price), 4, self.food1.id]]
        )  # [name, restaurant name, price per unit, quantity, food id]

    def test_get_fields(self):
        """
        Check that the model has the specified fields
        """
        raised = False
        try:
            self.order._meta.get_field('status')
            self.order._meta.get_field('user')
            self.order._meta.get_field('date_and_time')
            self.order._meta.get_field('cart')
        except FieldDoesNotExist:
            raised = True
        self.assertFalse(raised, 'One or more fields do not exist')
