from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from django.urls import reverse
from res_owner.models import Restaurant, Food, Category
from res_owner.forms import NewCategoryForm, CategorizingForm

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
class TestResHomePageViews(TestCase):
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

    def test_res_home_page_GET(self):
        """
        Test that the view function res_home_page accepts the GET request and renders the correct HTML page.
        """
        response = self.client.get(self.res_hp_view_func)
        # Assert that the request is successful
        self.assertEquals(response.status_code, 200)
        # Assert that the html page is used
        self.assertTemplateUsed(response, 'res_owner/res_home_page.html')

    def test_res_home_page_restaurant(self):
        """
        Test that the view function res_home_page includes the list of restaurants into
        the context before rendering the HTML page if the user has any.
        """
        response = self.client.get(self.res_hp_view_func)
        restaurant = Restaurant.objects.get(name='Almond')
        # Check if response's context contains the restaurants key
        self.assertTrue(response.context.get('restaurants'))
        # Check if the restaurants' value contains the restaurant
        self.assertTrue(restaurant in response.context['restaurants'])


class TestNewRestaurant(TestCase):
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

    def test_new_restaurant_GET(self):
        """
        Test that the view function new_restaurant accepts the GET request and renders the correct HTML page.
        """
        response = self.client.get(self.new_res_view_func)
        # Assert that the request is successful
        self.assertEquals(response.status_code, 200)
        # Assert that the html page is used
        self.assertTemplateUsed(response, 'res_owner/new_restaurant.html')

    def test_adding_a_restaurant_POST_success(self):
        """
        Test that the view function new_restaurant accepts the valid registration of a restaurant
        and makes sure it redirects to the appropriate page.
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


class TestNewFood(TestCase):
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

    def test_new_food_GET(self):
        """
        Test that the view function new_food accepts the GET request and renders the correct HTML page.
        """
        response = self.client.get(self.new_food_func)
        # Assert that the request is successful
        self.assertEquals(response.status_code, 200)
        # Assert that the html page is used
        self.assertTemplateUsed(response, 'res_owner/new_food.html')

    def test_new_food_POST_success(self):
        """
        Test that the view function new_food accepts the valid registration of a Food item and
        makes sure it redirects to the appropriate page.
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

    def test_new_food_POST_duplicate(self):
        """
        Test that the view function new_food rejects the registration of a Food item with the same name.
        This test is here instead of in test_forms because the database allows adding multiple food items
        of the same name. But a restaurant can only allow unique food names within that restaurant,
        and the corresponding view function handles that part.
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


class TestDeleteFood(TestCase):
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

    def test_delete_food_GET(self):
        """
        Test that the view function delete_food accepts the POST request and delete the Food item.
        """
        response = self.client.post(self.delete_food_func)

        # Assert that upon a successful completion of the code, the page is redirected to the restaurant page
        self.assertRedirects(response, self.restaurant_func, status_code=302)
        # Assert that the food actually gets obliterated off the database
        self.assertFalse(Food.objects.all())


class TestNewCategory(TestCase):
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
        self.restaurant = Restaurant.objects.create(
            name='Almond', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=self.user
        )
        self.food_one = Food.objects.create(
            name='Coral Worms', restaurant=self.restaurant,
            price=20,
            image_path='res_owner/images/coral_worm.png'
        )
        self.food_two = Food.objects.create(
            name='Worms Sushi BAWS special', restaurant=self.restaurant,
            price=30,
            image_path='res_owner/images/coral_worm.png'
        )
        self.res_hp_view_func = reverse(viewname='res_owner:res_home_page')
        self.new_cat_view_func = reverse(viewname='res_owner:new_category', args=[self.restaurant.id])

    def test_new_category_GET(self):
        """
        Test that the view function new_category accepts the GET request and renders the correct HTML page.
        """
        response = self.client.get(self.new_cat_view_func)
        # Assert that the request is successful
        self.assertEquals(response.status_code, 200)
        # Assert that the correct html page is used
        self.assertTemplateUsed(response, 'res_owner/new_category.html')

    def test_new_category_POST_success(self):
        """
        Test that the view function new_category accepts the valid registration of a Category and makes sure
        it redirects to the appropriate page.
        Currently non-functional due to the form_data to pass into the self.client.post being wonky because
        the NewCategoryForm has a ModelMultipleChoiceField. This works when testing on browsers but not in this test.
        """
        # When do client posting this time, the food has to be a list of food.id for MultipleChoiceField
        # the form_data is currently not working....
        form_data = {
            'name': 'Snail',
            'food': [str(self.food_one.id), str(self.food_two.id)],  # ID this time for MultipleChoiceField
        }

        response = self.client.post(self.new_cat_view_func, data=form_data)
        # Assert that upon a successful completion of the code, the page is redirected to the homepage
        self.assertRedirects(response, self.res_hp_view_func, status_code=302)
        # Assert that there is a Category created
        self.assertTrue(Category.objects.filter(name='Snail'))
        # Assert the restaurant and the food is associated with it
        self.assertTrue(self.restaurant.category_set.filter(name='Snail'))
        self.assertTrue(Category.objects.filter(name='Snail'))
        # Somehow the test doesn't work with ModelMultipleChoiceField. THIS IS NOT WORKING
        self.assertTrue(self.food_one.category_set.filter(name='Snail'))
        self.assertTrue(self.food_two.category_set.filter(name='Snail'))


        # self.assertTrue()
x
    # No testing duplicate that violates the unique key constraint.
    # since self.client.post basically bypassed through the forms.is_valid()
    # That should be the responsibility of the forms.is_valid() methinks


# class TestDeleteCategory(TestCase):
#     pass
#
#
# class TestCategorize(TestCase):
#     pass
