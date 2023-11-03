from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import *
from django.db.utils import IntegrityError
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
    def setUp(self):
        """
        Run once to set up non-modified data for all class methods
        """
        User = get_user_model()
        self.user = User.objects.create_user(email='iguanasalt@gmail.com',
                                        username='iguazu', is_res_owner=True,
                                        password='foo')
        # Create the restaurant object for testing.
        # user testing will run its own testing
        self.restaurant = Restaurant.objects.create(
            name='Almond', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=self.user
        )
        # Create a food object

    def test_get_fields(self):
        """
        Check that the model have the specified fields
        """
        raised = False
        try:
            self.restaurant._meta.get_field('name')
            self.restaurant._meta.get_field('location')
            self.restaurant._meta.get_field('image_path')
            self.restaurant._meta.get_field('restaurant_owner')
        except FieldDoesNotExist:
            raised = True
        self.assertFalse(raised, 'Some fields do not exist')

    def test_foreign_key_user(self):
        """
        Check that the model have the specified foreign key
        """
        self.assertEqual(self.restaurant.restaurant_owner.username, "iguazu")

    def test_max_length_of_fields(self):
        """
        Check to make sure all fields' max lengths values of this model
        are expected to equal specific numbers.
        """
        max_name_length = self.restaurant._meta.get_field('name').max_length
        max_location_length = self.restaurant._meta.get_field('location').max_length
        max_img_path_length = self.restaurant._meta.get_field('image_path').max_length
        self.assertEqual(max_name_length, 200)
        self.assertEqual(max_location_length, 200)
        self.assertEqual(max_img_path_length, 100)

    def test_unique_name(self):
        """
        Check that restaurant's name field is unique
        """
        self.raised = False
        try:
            Restaurant.objects.create(
                name='Almond', location='Earth-231',
                image_path='res_owner/images/Earth-231.png',
                restaurant_owner=self.user
            )
        except IntegrityError:
            self.raised = True
        self.assertTrue(self.raised)

    def test_delete(self):
        """
        Check to make sure that when the User is deleted, the restaurant associated with the User is also deleted as well
        """
        res_name = self.restaurant.name
        self.user.delete()
        # Assert that the restaurant got obliterated off the database
        self.assertFalse(Restaurant.objects.filter(name=res_name))


class TestFoodModel(TestCase):
    def setUp(self):
        """
        Run once to set up non-modified data for all class methods
        """
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='iguanasalt@gmail.com',
                                                  username='iguazu', is_res_owner=True,
                                                  password='foo')
        # Create the restaurant object for testing.
        # user testing will run its own testing
        self.restaurant = Restaurant.objects.create(
            name='Almondo', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=self.user
        )
        self.food = Food.objects.create(
            name='Coral Worms', restaurant=self.restaurant,
            price=20,
            image_path='res_owner/images/coral_worm.png'
        )

    def test_get_fields(self):
        """
        Check that the model have the specified fields
        """
        raised = False
        try:
            self.food._meta.get_field('name')
            self.food._meta.get_field('restaurant')
            self.food._meta.get_field('price')
            self.food._meta.get_field('image_path')
        except FieldDoesNotExist:
            raised = True
        self.assertFalse(raised, 'Some fields do not exist')

    def test_foreign_key_restaurant(self):
        """
        Check that the model have the specified foreign key
        """
        self.assertEqual(self.food.restaurant.name, "Almondo")

    def test_max_length_of_fields(self):
        """
            Check to make sure all fields' max lengths values of this model
            are expected to equal specific numbers.
        """
        max_name_length = self.food._meta.get_field('name').max_length
        max_price_digits = self.food._meta.get_field('price').max_digits
        max_img_path_length = self.food._meta.get_field('image_path').max_length
        self.assertEqual(max_name_length, 200)
        self.assertEqual(max_price_digits, 12)
        self.assertEqual(max_img_path_length, 100)

    def test_delete(self):
        """
        Check to make sure that when the Restaurant is deleted, the food associated with the restaurant is also deleted as well
        """
        food_name = self.food.name
        self.restaurant.delete()
        # Assert that the restaurant got obliterated off the database
        self.assertFalse(Food.objects.filter(name=food_name))


class TestCategory(TestCase):
    def setUp(self):
        """
        Run once to set up non-modified data for all class methods
        """
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='iguanasalt@gmail.com',
                                                  username='iguazu', is_res_owner=True,
                                                  password='foo')

        self.restaurant_1 = Restaurant.objects.create(
            name='Almondo', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=self.user
        )
        self.restaurant_2 = Restaurant.objects.create(
            name='Static Noise', location='Rubicon-231',
            image_path='res_owner/images/static-231.png',
            restaurant_owner=self.user
        )

        self.food_1 = Food.objects.create(
            name='Coral Worms', restaurant=self.restaurant_1,
            price=20,
            image_path='res_owner/images/coral_worm.png'
        )
        self.food_2 = Food.objects.create(
            name='Worms Sushi BAWS special', restaurant=self.restaurant_2,
            price=30,
            image_path='res_owner/images/coral_worm.png'
        )

        self.category = Category.objects.create(
            name='Worms',
        )
        self.category.food.add(self.food_1, self.food_2)
        self.category.restaurant.add(self.restaurant_1, self.restaurant_2)

    def test_get_fields(self):
        """
        Check that the model have the specified fields
        """
        raised = False
        try:
            self.category._meta.get_field('name')
            self.category._meta.get_field('restaurant')
            self.category._meta.get_field('food')
        except FieldDoesNotExist:
            raised = True
        self.assertFalse(raised, 'Some fields do not exist')

    def test_foreign_key_restaurant(self):
        """
        Check that the model have the specified key and that key represents the Many-to-Many field
        """
        self.assertTrue(self.category.restaurant.filter(name=self.restaurant_1.name) and
                        self.category.restaurant.get(name=self.restaurant_2.name))

    def test_foreign_key_food(self):
        """
        Check that the model have the specified key and that key represents the Many-to-Many field
        """
        self.assertTrue(self.category.food.filter(name=self.food_1.name) and
                        self.category.food.filter(name=self.food_2.name))

    def test_max_length_of_fields(self):
        """
            Check to make sure all fields' max lengths values of this model
            are expected to equal specific numbers.
        """
        max_name_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_name_length, 200)

    def test_unique_name(self):
        """
        Check that category's name field is unique
        """
        self.raised = False
        try:
            Category.objects.create(name='Worms')
        except IntegrityError:
            self.raised = True
        self.assertTrue(self.raised)

    def test_delete(self):
        """
        Check to make sure that when the category is deleted, nothing associated with it is also accidentally deleted
        """
        self.category.delete()
        # Assert no restaurants got obliterated off the database
        self.assertTrue(Restaurant.objects.filter(name=self.restaurant_1.name) and
                        Restaurant.objects.filter(name=self.restaurant_2.name))
        # Assert no food got obliterated off the database
        self.assertTrue(Food.objects.filter(name=self.food_1.name) and
                        Food.objects.filter(name=self.food_2.name))



