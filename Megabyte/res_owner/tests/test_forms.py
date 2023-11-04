from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from res_owner.models import Restaurant, Food, Category
from res_owner.forms import RestaurantForm, FoodForm, CategorizingForm, NewCategoryForm


class TestRestaurantForm(TestCase):
    def setUp(self):
        """
        Run once to set up non-modified data for all class methods
        """
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='iguanasalt@gmail.com',
                                                  username='iguazu', is_res_owner=True,
                                                  password='foo')
        self.restaurant = Restaurant.objects.create(
            name='Almond', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=self.user
        )

    def test_RestaurantForm_valid_data(self):
        """Test if RestaurantForm accepts specified valid data"""
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
        a_form = RestaurantForm(data={
            'name': 'G5-Iguana',
            'location': 'Rubicon-231',
            'image_path': 'res_owner/restaurants/iguana.png',
            'restaurant_owner': self.user
        })
        a_form.save()
        form = RestaurantForm(data={
            'name': 'G5-Iguana',
            'location': 'Rubicon-231',
            'image_path': 'res_owner/restaurants/iguana.png'
        })
        self.assertFalse(form.is_valid())

    def test_RestaurantForm_invalid_same_name(self):
        """
        Test if RestaurantForm rejects new entry with same name as an existing one in the database.
        """
        # Create an existing restaurant
        a_form = RestaurantForm(data={
            'name': 'G5-Iguana',
            'location': 'Rubicon-231',
            'image_path': 'res_owner/restaurants/iguana.png',
            'restaurant_owner': self.user
        })
        a_form.save()
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
        """Test if RestaurantForm rejects entry with missing data"""
        form = RestaurantForm(data={
            'location': 'Rubicon-3',
            'image_path': 'res_owner/restaurants/iguana.png'
        }
        )
        self.assertFalse(form.is_valid())


class TestFoodForm(TestCase):
    def setUp(self):
        """
        Run once to set up non-modified data for all class methods
        """
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='iguanasalt@gmail.com',
                                                  username='iguazu', is_res_owner=True,
                                                  password='foo')
        self.restaurant = Restaurant.objects.create(
            name='Almond', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=self.user
        )

    def test_FoodForm_valid_data(self):
        """Test if RestaurantForm accept specified valid data"""
        form = FoodForm(data={
            'name': 'Almond Milk',
            'restaurant': self.restaurant,
            'price': 21,
            'image_path': 'res_owner/foods/almond_milk.png'
        })
        self.assertTrue(form.is_valid())

    def test_FoodForm_missing_data(self):
        """Test if FoodForm rejects entry with missing data"""
        form = FoodForm(data={
            'name': 'Almond Milk',
            'restaurant': self.restaurant,
            'image_path': 'res_owner/foods/almond_milk.png'
        }
        )
        self.assertFalse(form.is_valid())


class TestNewCategoryForm(TestCase):
    def setUp(self):
        """
        Run once to set up non-modified data for all class methods
        """
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='iguanasalt@gmail.com',
                                                  username='iguazu', is_res_owner=True,
                                                  password='foo')
        self.restaurant = Restaurant.objects.create(
            name='Almond', location='Rubicon-231',
            image_path='res_owner/images/rubicon-231.png',
            restaurant_owner=self.user
        )
        self.food_1 = Food.objects.create(
            name='Coral Worms', restaurant=self.restaurant,
            price=20,
            image_path='res_owner/images/coral_worm.png'
        )
        self.food_2 = Food.objects.create(
            name='Worms Sushi BAWS special', restaurant=self.restaurant,
            price=30,
            image_path='res_owner/images/coral_worm.png'
        )

    def test_NewCategoryForm_valid_data(self):
        """Test if CategoryForm accept specified valid data"""
        form = NewCategoryForm(restaurant_id=self.restaurant.id, data={
            'name': 'Snail',
            'food': [self.food_1, self.food_2]  # It accepts a list
        })
        self.assertTrue(form.is_valid())

    def test_NewCategoryForm_valid_data_optional(self):
        """
        Test if NewCategoryForm can accept a new category entry without assigning any food item to it.
        """
        # Create an existing restaurant
        form = NewCategoryForm(restaurant_id=self.restaurant.id, data={
            'name': 'Snail',
            'food': []
        })

        self.assertTrue(form.is_valid)

    def test_NewCategoryForm_duplicate_data(self):
        """
        Test if NewCategoryForm rejects a new entry with the same name as an existing one in the database.
        """
        # Create an existing category
        form = NewCategoryForm(restaurant_id=self.restaurant.id, data={
            'name': 'Snail',
            'food': [self.food_1]
        })
        form.save()
        new_form = NewCategoryForm(restaurant_id=self.restaurant.id, data={
            'name': 'Snail',
            'food': [self.food_1, self.food_2]
        })
        self.assertFalse(new_form.is_valid())

    def test_NewCategoryForm_missing_data(self):
        """Test if NewCategoryForm rejects entry with missing data that is not optional"""
        form = NewCategoryForm(restaurant_id=self.restaurant.id, data={
            'food': [self.food_1]
        }
        )
        self.assertFalse(form.is_valid())
# CategorizingForm is in the jurisdiction of their respective views function as it is used to assign food items
# to a category record
