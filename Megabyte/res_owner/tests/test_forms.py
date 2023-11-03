from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from res_owner.models import Restaurant, Food, Category
from res_owner.forms import RestaurantForm, FoodForm, CategorizingForm, NewCategoryForm


class TestResOwnerForms(TestCase):
    def setUp(self):
        """
        Run once to set up non-modified data for all class methods
        """
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='iguanasalt@gmail.com',
                                                  username='iguazu', is_res_owner=True,
                                                  password='foo')
        self.restaurant = Restaurant.objects.create(
            name='Almond', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=self.user
        )
        self.client.login(email='iguanasalt@gmail.com', password='foo')
        self.res_hp_view_func = reverse(viewname='res_owner:res_home_page')
        self.new_res_view_func = reverse(viewname='res_owner:new_restaurant')

    def test_RestaurantForm_valid_data(self):
        """Test if RestaurantForm accept specified valid data"""
        form = RestaurantForm(data={
            'name': 'G5-Iguana',
            'location': 'Rubicon-3',
            'image_path': 'res_owner/restaurants/iguana.png'
        }
        )
        self.assertTrue(form.is_valid())

    def test_RestaurantForm_duplicate_data(self):
        """
        Test if RestaurantForm rejects duplicate data
        """
        # Create an existing restaurant
        response = self.client.post(self.new_res_view_func, {
            'name': 'G5-Iguana',
            'location': 'Rubicon-231',
            'image_path': 'res_owner/restaurants/iguana.png',
            'restaurant_owner': self.user
        })
        form = RestaurantForm(data={
            'name': 'G5-Iguana',
            'location': 'Rubicon-231',
            'image_path': 'res_owner/restaurants/iguana.png'
        })
        self.assertFalse(form.is_valid())

    def test_RestaurantForm_invalid_data(self):
        """
        Test if RestaurantForm rejects data with same name
        """
        # Create an existing restaurant
        response = self.client.post(self.new_res_view_func, {
            'name': 'G5-Iguana',
            'location': 'Rubicon-231',
            'image_path': 'res_owner/restaurants/iguana.png',
            'restaurant_owner': self.user
        })
        form = RestaurantForm(data={
            'name': 'G5-Iguana',
            'location': 'Hearthian',
            'image_path': 'res_owner/restaurants/iguana.png'
        })
        self.assertFalse(form.is_valid())
        # Assert there is an error in form and that the error is in the duplicate name
        self.assertEquals(len(form.errors), 1)
        self.assertTrue(form.errors.get('name'))

    def test_RestaurantForm_missing_data(self):
        """Test if RestaurantForm rejects data with missing data"""
        form = RestaurantForm(data={
            'location': 'Rubicon-3',
            'image_path': 'res_owner/restaurants/iguana.png'
        }
        )
        self.assertFalse(form.is_valid())
        # Assert there is an error in form and that the error is in the duplicate name
        self.assertEquals(len(form.errors), 1)
        self.assertTrue(form.errors.get('name'))


class TestAddingFoodForm(TestCase):
    def setUp(self):
        """
        Run once to set up non-modified data for all class methods
        """
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='iguanasalt@gmail.com',
                                                  username='iguazu', is_res_owner=True,
                                                  password='foo')
        self.restaurant = Restaurant.objects.create(
            name='Almond', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=self.user
        )
        self.client.login(email='iguanasalt@gmail.com', password='foo')

    def test_FoodForm_valid_data(self):
        """Test if RestaurantForm accept specified valid data"""
        form = FoodForm(data={
            'name': 'Almond Milk',
            'restaurant': self.restaurant,
            'price': 21,
            'image_path': 'res_owner/foods/almond_milk.png'
        })
        self.assertTrue(form.is_valid())


class TestNewCategoryForm(TestCase):
    pass


class TestCategorizingForm(TestCase):
    pass
