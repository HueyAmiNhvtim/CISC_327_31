from django.contrib.auth import get_user_model
from django.core.exceptions import *
from user.forms import *
from res_owner.models import Restaurant, Category, Food

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class TestUser(LiveServerTestCase):
    '''
    @classmethod
    def setUpClass(cls):
        cls.CustomUserModel = get_user_model()
        super().setUpClass()
        cls.chrome_webdriver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.chrome_webdriver.quit()
        super().tearDownClass()
    '''

    def setUp(self):
        self.User = get_user_model()
        # Create user and owner accounts
        
        self.user = self.User.objects.create_user(email='test_user@gmail.com', 
                                                  username='test_User', is_res_owner=False, 
                                                  password='IAmAUs3r')
        self.res_owner1 = self.User.objects.create_user(email='test_owner1@gmail.com', 
                                                  username='test_owner1', is_res_owner=True, 
                                                  password='IAmAn0wner')
        self.res_owner2 = self.User.objects.create_user(email='test_owner2@gmail.com', 
                                                  username='test_owner2', is_res_owner=True, 
                                                  password='IAmAn0wner')
        self.res_1 = Restaurant.objects.create(name='Fruit Market', 
                                  location='123 Main Street,City,Province,Country,123 ABC', 
                                  image_path='FruitMarket.png', restaurant_owner=self.res_owner1)
        self.res_2 = Restaurant.objects.create(name='Dollar Store', 
                                  location='124 Main Street,City,Province,Country,123 ABD', 
                                  image_path='DollarStore.png', restaurant_owner=self.res_owner1)
        self.res_3 = Restaurant.objects.create(name='Fruit Empire', 
                                  location='125 Main Street,City,Province,Country,123 ABE', 
                                  image_path='FruitEmpire.png', restaurant_owner=self.res_owner2)
        self.food_1 = Food.objects.create(name='Apple', restaurant=self.res_1,
                                           price=1.00, image_path='Apple.png')
        self.food_2 = Food.objects.create(name='Banana', restaurant=self.res_1,
                                           price=0.50, image_path='Banana.png')
        self.cat_1 = Category.objects.create(name='Fruits')
        self.cat_1.food.add(self.food_1)
        self.cat_1.food.add(self.food_2)
        
        
    def test_user(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        ##################
        ##  LOGIN PAGE  ##
        ##################

        # Get input fields
        email_input = driver.find_element(By.NAME, 'username') # 'username' is due to it being a unique identifier
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')

        # Enter login info
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        # Submit
        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        ######################
        ##  USER HOME PAGE  ##
        ######################

        # Verify that the user has been redirected to the user home page
        assert driver.current_url == 'http://127.0.0.1:8000/%5Ehome/$' or driver.current_url == 'http://127.0.0.1:8000/user/' or driver.current_url == 'http://127.0.0.1:8000/home/'

        # Verify that user's username is displayed correctly on the home page
        assert 'Hello, test_User' in driver.page_source

        search_button = driver.find_element(By.NAME, 'search_button')
        search_button.click()

        time.sleep(1)

        ###################
        ##  SEARCH PAGE  ##
        ###################

        # Verify that the user has been redirected to the search page
        assert driver.current_url == 'http://127.0.0.1:8000/user/search'
        
        # Verify that the search page has loaded correctly
        assert 'Please enter your location to begin searching for restaurants in your local area.' in driver.page_source

        # Get search fields
        street_input = driver.find_element(By.NAME, 'street')
        city_input = driver.find_element(By.NAME, 'city')
        province_or_state_input = driver.find_element(By.NAME, 'province_or_state')
        country_input = driver.find_element(By.NAME, 'country')
        postal_code_input = driver.find_element(By.NAME, 'postal_code')
        search_button2 = driver.find_element(By.NAME, 'search_button')

        # Enter search info
        street_input.send_keys('21-25 Union Street')
        city_input.send_keys('Kingston')
        province_or_state_input.send_keys('Ontario')
        country_input.send_keys('Canada')
        postal_code_input.send_keys('K7L 2N8')
        
        # Submit
        search_button2.send_keys(Keys.RETURN)
        
        time.sleep(1)

        ###########################
        ##  SEARCH RESULTS PAGE  ##
        ###########################

        # Verify that the user has been redirected to the search results page
        assert driver.current_url == 'http://127.0.0.1:8000/user/search_results/'

        # Verify that the search results page has loaded correctly
        assert 'Search Results' in driver.page_source

        # Verify that the restaurants created upon set-up appear 
        # in the search results. A NoSuchElementException is 
        # raised if a restaurant is not found.
        restaurant_1 = driver.find_element(By.LINK_TEXT, 'Fruit Market')
        # Error due to views not updating with new objects
        restaurant_2 = driver.find_element(By.LINK_TEXT, 'Dollar Store')
        restaurant_3 = driver.find_element(By.LINK_TEXT, 'Fruit Empire')

        # Go to restaurant 1 (Fruit Market)'s page
        restaurant_1.click()

        time.sleep(1)
        
        #######################
        ##  RESTAURANT PAGE  ##
        #######################

        # Verify that the user has been redirected to the restaurant's menu page
        restaurant_1_id = self.res_1.id
        assert driver.current_url == 'http://127.0.0.1:8000/user/restaurant/{}'.format(restaurant_1_id)

        # Verify that the restaurant page has loaded correctly
        assert 'Fruit Market Categories' in driver.page_source

        category_1 = driver.find_element(By.LINK_TEXT, 'Fruits')

        # Go to category 1 (Fruits)
        category_1.click()

        time.sleep(1)

        #####################
        ##  CATEGORY PAGE  ##
        #####################

        # Verify that the user has been redirected to the category's page
        assert driver.current_url == 'http://127.0.0.1:8000/user/restaurant/{}/Fruits'.format(restaurant_1_id)

        # Verify that the category page has been loaded correctly
        assert 'Viewing Fruits in Fruit Market' in driver.page_source

        # Verify that the food items created upon set-up appear 
        # in the search results. A NoSuchElementException is 
        # raised if a restaurant is not found.
        food_1 = driver.find_element(By.LINK_TEXT, 'Apple $1.000000') # Still has trailing zeros
        
        # Same error due to views not updating the objects
        food_2 = driver.find_element(By.LINK_TEXT, 'Banana $0.500000')

        # Go to food 1 (Apple)'s page
        food_1.click()

        time.sleep(1)

        #################
        ##  FOOD PAGE  ##
        #################

        # Verify that the user has been redirected to the food item's page
        assert driver.current_url == 'http://127.0.0.1:8000/user/restaurant/{}/Fruits/Apple'.format(restaurant_1_id)

        # Verify that the food page has been loaded correctly
        assert 'How many would you like to buy?' in driver.page_source

        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Add 5 of food 1 (Apple) to the user's cart
        quantity_input.send_keys('5')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        ##########################
        ##  SHOPPING CART PAGE  ##
        ##########################

        # Verify that the user has been redirected to their shopping cart
        assert driver.current_url == 'http://127.0.0.1:8000/user/shopping_cart/'

        # Verify that the shopping cart page has been loaded correctly
        assert 'Shopping Cart' in driver.page_source

        # Verify that added items and their properties are displayed
        assert 'Item: Apple' in driver.page_source
        assert 'Restaurant: Fruit Market' in driver.page_source
        assert 'Price per item: $1.000000' in driver.page_source
        assert 'Quantity: 5' in driver.page_source

        # Store food id for later

        # This is not a good solution and will fail in production
        food_1_id = 1

        # This test works because it is being tested with one item in the cart
        # If there are multiple, there will need to be workarounds to test it
        edit = driver.find_element(By.NAME, 'edit_button')

        # Go to the edit page of food 1 (Apple)
        edit.click()

        time.sleep(1)

        ##########################
        ##  EDIT QUANTITY PAGE  ##
        ##########################

        # Verify that the user has been redirected to the edit quantity page
        # This is to ignore the generated csrftoken in the url
        edit_quantity_url_length = 46 + len(str(food_1_id))
        assert driver.current_url[:edit_quantity_url_length] == 'http://127.0.0.1:8000/user/shopping_cart/edit/{}'.format(food_1_id)

        # Verify that the shopping cart page has been loaded correctly
        assert 'Edit Quantity' in driver.page_source

        quantity_2_input = driver.find_element(By.NAME, 'quantity')
        edit_quantity_2 = driver.find_element(By.NAME, 'edit_quantity_button')

        # Change quantity of food 1 (Apple) to 2
        quantity_2_input.send_keys('2')
        edit_quantity_2.send_keys(Keys.RETURN)

        time.sleep(1)

        #############################
        ##  SHOPPING CART PAGE (2) ##
        #############################

        # Verify that the user has been redirected to their shopping cart
        assert driver.current_url == 'http://127.0.0.1:8000/user/shopping_cart/'

        # Verify that the shopping cart page has been loaded correctly
        assert 'Shopping Cart' in driver.page_source

        # Verify that quantity of food 1 (Apple) has been changed to 2
        assert 'Quantity: 2' in driver.page_source

        # This test works because it is being tested with one item in the cart
        # If there are multiple, there will need to be workarounds to test it
        remove_food = driver.find_element(By.NAME, 'remove_food_button')

        # Remove food 1 (Apple) from the shopping cart
        remove_food.click()

        time.sleep(1)

        # Verify that food 1 (Apple) has been removed from display
        assert 'Item: Apple' not in driver.page_source
        assert 'Restaurant: Fruit Market' not in driver.page_source
        assert 'Price per item: $1.000000' not in driver.page_source
        assert 'Quantity: 2' not in driver.page_source

        # Navigate to user home page
        home = driver.find_element(By.LINK_TEXT, 'Home')
        home.click()

        time.sleep(1)

        #########################
        ##  USER HOME PAGE (2) ##
        #########################

        # Verify that the user has been redirected to the user home page
        assert driver.current_url == 'http://127.0.0.1:8000/%5Ehome/$' or driver.current_url == 'http://127.0.0.1:8000/user/' or driver.current_url == 'http://127.0.0.1:8000/home/'

        # Go through add to cart process again
        search_button = driver.find_element(By.NAME, 'search_button')
        search_button.click()
        time.sleep(1)
        # Search
        street_input = driver.find_element(By.NAME, 'street')
        city_input = driver.find_element(By.NAME, 'city')
        province_or_state_input = driver.find_element(By.NAME, 'province_or_state')
        country_input = driver.find_element(By.NAME, 'country')
        postal_code_input = driver.find_element(By.NAME, 'postal_code')
        search_button2 = driver.find_element(By.NAME, 'search_button')
        street_input.send_keys('21-25 Union Street')
        city_input.send_keys('Kingston')
        province_or_state_input.send_keys('Ontario')
        country_input.send_keys('Canada')
        postal_code_input.send_keys('K7L 2N8')
        search_button2.send_keys(Keys.RETURN)
        time.sleep(1)
        # Search results
        restaurant_1 = driver.find_element(By.LINK_TEXT, 'Fruit Market')
        restaurant_1.click()
        time.sleep(1)
        # Restaurant
        category_1 = driver.find_element(By.LINK_TEXT, 'Fruits')
        category_1.click()
        time.sleep(1)
        # Category
        food_1 = driver.find_element(By.LINK_TEXT, 'Apple $1.000000')
        food_1.click()
        time.sleep(1)
        # Food
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')
        quantity_input.send_keys('2')
        add_to_cart.send_keys(Keys.RETURN)
        time.sleep(1)

        #############################
        ##  SHOPPING CART PAGE (3) ##
        #############################

        # Verify that the shopping cart page has been loaded correctly
        assert 'Shopping Cart' in driver.page_source

        # Checkout
        checkout = driver.find_element(By.NAME, 'checkout_button')
        checkout.click()

        time.sleep(1)

        ########################
        ##  VIEW ORDERS PAGE  ##
        ########################

        # Verify that the user has been redirected to the orders page
        assert driver.current_url == 'http://127.0.0.1:8000/user/view_orders'

        # Verify that the orders page has been loaded correctly
        assert 'Orders' in driver.page_source

        # This test works because it is being tested with one existing order
        # If there are multiple, there will need to be workarounds to test it
        links = driver.find_elements(By.TAG_NAME, 'a')
        order_link = links[1].get_attribute('href')
        order_id = order_link[order_link.rindex('/') + 1:]
        
        # Go to order details
        links[1].click()

        time.sleep(1)

        ##################
        ##  ORDER PAGE  ##
        ##################

        # Verify that the user has been redirected to the orders page
        time.sleep(10)
        assert driver.current_url == 'http://127.0.0.1:8000/user/view_orders/{}'.format(order_id)

        # Verify that the orders page has been loaded correctly
        assert 'Order #{}'.format(order_id) in driver.page_source

        # Verify that purchased items and their properties are displayed
        assert 'Item: Apple' in driver.page_source
        assert 'Restaurant: Fruit Market' in driver.page_source
        assert 'Price per item: $1.000000' in driver.page_source
        assert 'Quantity: 2' in driver.page_source