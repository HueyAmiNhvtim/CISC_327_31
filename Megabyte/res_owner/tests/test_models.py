from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import *
from res_owner.models import Restaurant, Food, Category


# Create your tests here blin.
# Often you will add a test class for each model/view/form you want to test,
# with individual methods for testing specific functionality. In other cases
# you may wish to have a separate class for testing a specific use case, with
# individual test functions that test aspects of that use-case (for example,
# a class to test that a model field is properly validated, with functions to
# test each of the possible failure cases). Again, the structure is very much
# up to you, but it is best if you are consistent.


# python3 manage.py test --verbosity 2
# python3 manage.py test --parallel auto if tests are independent...
class TestRestaurantModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Run once to set up non-modified data for all class methods
        """
        User = get_user_model()
        user = User.objects.create_user(email='iguanasalt@gmail.com',
                                        username='iguazu', is_res_owner=True,
                                        password='foo')
        # Create the restaurant object for testing.
        # user testing will run its own testing
        Restaurant.objects.create(
            name='Almond', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=user
        )
        # Create a food object

    def test_get_fields(self):
        """
        Check that the model have the specified fields
        """
        restaurant = Restaurant.objects.get(id=1)
        raised = False
        try:
            restaurant._meta.get_field('name')
            restaurant._meta.get_field('location')
            restaurant._meta.get_field('image_path')
            restaurant._meta.get_field('restaurant_owner')
        except FieldDoesNotExist:
            raised = True
        self.assertFalse(raised, 'Some fields do not exist')

    def test_max_length_of_fields(self):
        """
        Check to make sure all fields' max lengths values of this model
        are expected to equal specific numbers.
        """
        restaurant = Restaurant.objects.get(id=1)
        max_name_length = restaurant._meta.get_field('name').max_length
        max_location_length = restaurant._meta.get_field('location').max_length
        max_img_path_length = restaurant._meta.get_field('image_path').max_length
        self.assertEqual(max_name_length, 200)
        self.assertEqual(max_location_length, 200)
        self.assertEqual(max_img_path_length, 100)


class TestFoodModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Run once to set up non-modified data for all class methods
        """
        User = get_user_model()
        user = User.objects.create_user(email='iguanasalt@gmail.com',
                                        username='iguazu', is_res_owner=True,
                                        password='foo')
        # Create the restaurant object for testing.
        # user testing will run its own testing
        restaurant = Restaurant.objects.create(
            name='Almond', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=user
        )

    def test_get_fields(self):
        """
        Check that the model have the specified fields
        """
        restaurant = Restaurant.objects.get(id=1)
        raised = False
        try:
            restaurant._meta.get_field('name')
            restaurant._meta.get_field('location')
            restaurant._meta.get_field('image_path')
            restaurant._meta.get_field('restaurant_owner')
        except FieldDoesNotExist:
            raised = True
        self.assertFalse(raised, 'Some fields do not exist')

    def test_max_length_of_fields(self):
        """
        Check to make sure all fields' max lengths values of this model
        are expected to equal specific numbers.
        """
        restaurant = Restaurant.objects.get(id=1)
        max_name_length = restaurant._meta.get_field('name').max_length
        max_location_length = restaurant._meta.get_field('location').max_length
        max_img_path_length = restaurant._meta.get_field('image_path').max_length
        self.assertEqual(max_name_length, 200)
        self.assertEqual(max_location_length, 200)
        self.assertEqual(max_img_path_length, 100)

