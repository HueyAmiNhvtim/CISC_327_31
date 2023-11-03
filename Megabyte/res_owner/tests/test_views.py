from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from django.urls import reverse
from res_owner.models import Restaurant, Food, Category


# NOTE: THIS IS INEFFICIENT due to the overhead cost of creating the dummy database and all the other stuff
# in each class.setUp... and I will fix it later when I have the time

# something like
# We should have make food have a many-to-many relationship to restaurant man...... But that's just a QOL....

# Restaurants shenanigans
# Test if adding restaurant will make the restaurant appear in the database.
# Test if removing restaurant will delete that restaurant alongside its associating food in the database

# Food shenanigans
# Test if pressing delete will delete the actual food off the restaurant

# Test redirects too lol for every views that can redirect
# Test if template exists too lol.


# Category shenanigans, a lof this feels like unit-testing tbh....
# Right now we just have to do requirements testing.
# Test to see if uncategorized food actually appear in the Others section
# Test if recategorized food actually appear in the new category
# Test if food with multiple categories will appear in both categories
# Test if deleting category will move food with only one category to go back to Others
# # Test to see if foods from other restaurants will appear in the
# # same category as other restaurants
# Test if a restaurant can use the same category for their food
class TestRestaurantOwnerHomePageViews(TestCase):
    def setUp(self):
        """
        Run once to set up non-modified data for all class methods
        """
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='iguanasalt@gmail.com',
                                                  username='iguazu', is_res_owner=True,
                                                  password='foo')
        self.client.login(email='iguanasalt@gmail.com', password='foo')
        # Create the restaurant object for testing.
        # user testing will run its own testing
        Restaurant.objects.create(
            name='Almond', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=self.user
        )
        self.res_hp_view_func = reverse(viewname='res_owner:res_home_page')

    def test_restaurants_home_page_GET(self):
        """
        Test that the page res_home_page.html accepts the requests and render the correct html page
        """
        response = self.client.get(self.res_hp_view_func)
        # Assert that the request is successful
        self.assertEquals(response.status_code, 200)
        # Assert that the html page is used
        self.assertTemplateUsed(response, 'res_owner/res_home_page.html')

    def test_restaurants_home_page_restaurant(self):
        """
        Test that the view function renders the res_home_page.html with the context of restaurant
        """
        response = self.client.get(self.res_hp_view_func)
        restaurant = Restaurant.objects.get(name='Almond')
        # Check if response's context contains the restaurants key
        self.assertTrue(response.context.get('restaurants'))
        # Check if the restaurants' value contains the restaurant
        self.assertTrue(restaurant in response.context['restaurants'])


class TestAddingARestaurant(TestCase):
    def setUp(self):
        """
        Run once to set up non-modified data for all class methods
        """
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='iguanasalt@gmail.com',
                                                  username='iguazu', is_res_owner=True,
                                                  password='foo')
        self.client.login(email='iguanasalt@gmail.com', password='foo')
        self.res_hp_view_func = reverse(viewname='res_owner:res_home_page')
        self.new_res_view_func = reverse(viewname='res_owner:new_restaurant')

    def test_adding_a_restaurant_GET(self):
        """
        Test that the page new_restaurant.html accepts the GET request and render the correct html page
        """
        response = self.client.get(self.new_res_view_func)
        # Assert that the request is successful
        self.assertEquals(response.status_code, 200)
        # Assert that the html page is used
        self.assertTemplateUsed(response, 'res_owner/new_restaurant.html')

    def test_adding_a_restaurant_POST_success(self):
        """
        Test that the page new_restaurant.html accepts the registration a restaurant with valid data
        """
        response = self.client.post(self.new_res_view_func, {
            'name': 'Almond',
            'location': 'Rubicon-231',
            'image_path': 'res_owner/images/rubicon-231.png',
            'restaurant_owner': self.user
        })

        # Assert that upon a successful completion of the code, the page is redirected to the homepage
        self.assertRedirects(response, self.res_hp_view_func, status_code=302)
        # Assert that there is a restaurant associated with the User
        self.assertTrue(self.user.restaurant_set.filter(name='Almond'))

    # No testing duplicate that violates the unique key constraint.
    # since self.client.post basically bypassed through the forms.is_valid()
    # That should be the responsibility of the forms.is_valid() methinks


class TestAddingFood(TestCase):
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
        # 1 for the id of the restaurant created
        self.res_hp_view_func = reverse(viewname='res_owner:res_home_page')
        self.new_food_func = reverse(viewname='res_owner:new_food', args=[1])

    def test_adding_food_GET(self):
        """
        Test that the page new_food.html accepts the GET requests and render the correct html page
        """
        response = self.client.get(self.new_food_func)
        # Assert that the request is successful
        self.assertEquals(response.status_code, 200)
        # Assert that the html page is used
        self.assertTemplateUsed(response, 'res_owner/new_food.html')

    def test_adding_food_POST_success(self):
        """
        Test that the page new_food.html accepts the registration a restaurant with valid data
        """
        response = self.client.post(self.new_food_func, {
            'name': 'Almond Milk',
            'restaurant': self.restaurant,
            'price': 20,
            'image_path': 'res_owner/foods/almond_milk.png'
        })

        # Assert that upon a successful completion of the code, the page is redirected to the homepage
        self.assertRedirects(response, self.res_hp_view_func, status_code=302)
        # Assert that there is a restaurant associated with the User
        self.assertTrue(self.restaurant.food_set.filter(name='Almond Milk'))

    def test_adding_food_POST_duplicate(self):
        """
        This test is in here instead of in test_forms because database allows adding multiple food items of same name
        But a restaurant can only have a single food with same name, and the corresponding view function
        handles that part.
        """
        response = self.client.post(self.new_food_func, {
            'name': 'Almond Milk',
            'restaurant': self.restaurant,
            'price': 20,
            'image_path': 'res_owner/foods/almond_milk.png'
        })

        response_2 = self.client.post(self.new_food_func, {
            'name': 'Almond Milk',
            'restaurant': self.restaurant,
            'price': 21,
            'image_path': 'res_owner/foods/almond_milk.png'
        })

        # Assert that upon an unsuccessful post, the page will just be rendered again
        self.assertEqual(response_2.status_code, 200)
        # Assert that the price of Food is still unchanged
        self.assertEqual(Food.objects.get(name='Almond Milk').price, 20)


class TestRemovingFood(TestCase):
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
        self.food = Food.objects.create(name='Almond Milk',
                                        restaurant=self.restaurant,
                                        price=21,
                                        image_path='res_owner/foods/almond_milk.png')
        self.client.login(email='iguanasalt@gmail.com', password='foo')
        # 1 for the id of the restaurant created
        self.delete_food_func = reverse(viewname='res_owner:delete_food', args=[1])
        self.restaurant_func = reverse(viewname='res_owner:restaurant', args=[self.restaurant.id])

    def test_deleting_food_GET(self):
        """
        Test that if delete_food accepts the GET requests
        """
        response = self.client.post(self.delete_food_func)

        # Assert that upon a successful completion of the code, the page is redirected to the restaurant page
        self.assertRedirects(response, self.restaurant_func, status_code=302)
        # Assert that the food actually gets obliterated off the database
        self.assertFalse(Food.objects.all())


class TestCreateCategory(TestCase):
    pass


class TestDeleteCategory(TestCase):
    pass


class TestCategorize(TestCase):
    pass
