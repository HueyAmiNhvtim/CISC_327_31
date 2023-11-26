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

        
    def test_add_under_min_quantity(self):
        """
        Add to cart with invalid quantity, quantity is below minumum of 1

        Input
        Quantity: -1
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to food page
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Add -1 items to the user's cart
        quantity_input.send_keys('-1')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Check that the user was not redirected
        self.assertTrue(driver.current_url == 'http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple', 
                         "User was redirected with invalid Quantity form entry")

        # Check that some error message is displayed
        self.assertTrue("ERROR: Quantity must be greater than 0." in driver.page_source,
                        "Error message was not displayed")

        # check that it was not added to the cart
        driver.get('http://127.0.0.1:8000/user/shopping_cart')
        self.assertTrue('Item: Apple' not in driver.page_source, 
                        "Shopping cart was updated with invalid Quantity form entry")
        
        if 'Item: Apple' in driver.page_source:
            # Remove food from cart so that it does not affect other test cases
            remove_food = driver.find_element(By.NAME, 'remove_food_button')
            remove_food.click()

    def test_add_over_max_quantity(self):
        """
        Add to cart with invalid quantity, quantity is above manimum of 100

        Input
        Quantity: 101
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to food page
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Try to add 101 items to the user's cart
        quantity_input.send_keys('101')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Check that the user was not redirected
        self.assertTrue(driver.current_url == 'http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple', 
                         "User was redirected with invalid Quantity form entry")

        # Check that some error message is displayed
        self.assertTrue("ERROR: Quantity must be less than 101." in driver.page_source, 
                        "Error message was not displayed")

        # check that it was not added to the cart
        driver.get('http://127.0.0.1:8000/user/shopping_cart')
        self.assertTrue('Item: Apple' not in driver.page_source, 
                        "Shopping cart was updated with invalid Quantity form entry")
        
        if 'Item: Apple' in driver.page_source:
            # Remove food from cart so that it does not affect other test cases
            remove_food = driver.find_element(By.NAME, 'remove_food_button')
            remove_food.click()

    def test_add_valid_quantity_non_existing(self):
        """
        Regular case with valid quantity with no existing
        amount of the item in the shopping cart
        
        Input
        Quantity: 5
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to food page
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Add 5 items to the user's cart
        quantity_input.send_keys('5')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Check that the user was redirected
        self.assertTrue(driver.current_url == 'http://127.0.0.1:8000/user/shopping_cart/', "User was not redirected")

        # Verify that the item has been sucessfully added to the user's cart
        assert 'Item: Apple' in driver.page_source
        assert 'Restaurant: Fruit Market' in driver.page_source
        assert 'Price per item: $1.000000' in driver.page_source
        assert 'Quantity: 5' in driver.page_source

        # Remove food from cart so that it does not affect other test cases
        remove_food = driver.find_element(By.NAME, 'remove_food_button')
        remove_food.click()

    def test_add_valid_quantity_existing(self):
        """
        Regular case with valid quantity with no existing
        amount of the item in the shopping cart
        
        Input
        Quantity: 4
        Existing: True
        In cart: 1
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to food page
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Add 1 item to the user's cart
        quantity_input.send_keys('1')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Navigate to food page again
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Add 4 more of that item to the user's cart
        quantity_input.send_keys('4')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Check that the user was redirected
        self.assertTrue(driver.current_url == 'http://127.0.0.1:8000/user/shopping_cart/', "User was not redirected")

        # Verify that the item has been sucessfully added to the user's cart
        assert 'Item: Apple' in driver.page_source
        assert 'Restaurant: Fruit Market' in driver.page_source
        assert 'Price per item: $1.000000' in driver.page_source
        assert 'Quantity: 5' in driver.page_source

        # Remove food from cart so that it does not affect other test cases
        remove_food = driver.find_element(By.NAME, 'remove_food_button')
        remove_food.click()

    def test_add_valid_quantity_existing_overflow(self):
        """
        Add to cart with invalid quantity, as adding this amount to the shopping 
        cart brings the amount of that item to a number greater than 100

        Input
        Quantity: 100
        Existing: True
        In cart: 1
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to food page
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Add 1 item to the user's cart
        quantity_input.send_keys('1')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Navigate to food page again
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Try to add 100 more of that item to the user's cart
        quantity_input.send_keys('100')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Check that the user was not redirected
        self.assertTrue(driver.current_url == 'http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple', 
                         "User was redirected with invalid Quantity form entry")

        # Check that some error message is displayed
        self.assertTrue("ERROR: Quantity in shopping cart must not exceed 100." in driver.page_source, 
                        "Error message was not displayed")

        # check that it was not changes the cart
        driver.get('http://127.0.0.1:8000/user/shopping_cart')
        self.assertTrue('Quantity: 101' not in driver.page_source, 
                        "Shopping cart was updated with invalid Quantity form entry")
        
        if 'Item: Apple' in driver.page_source:
            # Remove food from cart so that it does not affect other test cases
            remove_food = driver.find_element(By.NAME, 'remove_food_button')
            remove_food.click()

    def test_edit_quantity_valid(self):
        """
        Edit quantity of an item in the cart with a valid quantity

        Input:
        Quantity: 8
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to food page
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Add 1 item to the user's cart
        quantity_input.send_keys('1')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Go to the edit page of the food item
        edit = driver.find_element(By.NAME, 'edit_button')
        edit.click()

        time.sleep(1)

        quantity_2_input = driver.find_element(By.NAME, 'quantity')
        edit_quantity_2 = driver.find_element(By.NAME, 'edit_quantity_button')

        # Change quantity of the food item to 8
        quantity_2_input.send_keys('8')
        edit_quantity_2.send_keys(Keys.RETURN)

        time.sleep(1)

        # Check that the user was redirected
        self.assertTrue(driver.current_url == 'http://127.0.0.1:8000/user/shopping_cart/', 
                        "User was not redirected")

        # Verify that the quantity of the food item has been sucessfully changed in the user's cart
        assert 'Item: Apple' in driver.page_source
        assert 'Restaurant: Fruit Market' in driver.page_source
        assert 'Price per item: $1.000000' in driver.page_source
        assert 'Quantity: 8' in driver.page_source

        # Remove food from cart so that it does not affect other test cases
        remove_food = driver.find_element(By.NAME, 'remove_food_button')
        remove_food.click()

    def test_edit_under_min_quantity(self):
        """
        Edit quantity of an item in the cart with a quantity under 1

        Input:
        Quantity: -1
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to food page
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Store food id
        food_id = 1

        # Add 1 item to the user's cart
        quantity_input.send_keys('1')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Go to the edit page of the food item
        edit = driver.find_element(By.NAME, 'edit_button')
        edit.click()

        time.sleep(1)

        quantity_2_input = driver.find_element(By.NAME, 'quantity')
        edit_quantity_2 = driver.find_element(By.NAME, 'edit_quantity_button')

        # Change quantity of the food item to -1
        quantity_2_input.send_keys('-1')
        edit_quantity_2.send_keys(Keys.RETURN)

        time.sleep(1)

        # Check that the user was not redirected
        edit_quantity_url_length = 46 + len(str(food_id))
        assert driver.current_url[:edit_quantity_url_length] == 'http://127.0.0.1:8000/user/shopping_cart/edit/{}'.format(food_id)

        # Check that some error message is displayed
        self.assertTrue("ERROR: New quantity must be greater than 0." in driver.page_source, 
                        "Error message was not displayed")

        # check that quantity was not updated
        driver.get('http://127.0.0.1:8000/user/shopping_cart')
        self.assertTrue('Quantity: 1' in driver.page_source, 
                        "Shopping cart was updated with invalid Quantity form entry")
        
        # Remove food from cart so that it does not affect other test cases
        remove_food = driver.find_element(By.NAME, 'remove_food_button')
        remove_food.click()

    def test_edit_over_max_quantity(self):
        """
        Edit quantity of an item in the cart with a quantity over 100

        Input:
        Quantity: 101
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to food page
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Store food id
        food_id = 1

        # Add 1 item to the user's cart
        quantity_input.send_keys('1')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Go to the edit page of the food item
        edit = driver.find_element(By.NAME, 'edit_button')
        edit.click()

        time.sleep(1)

        quantity_2_input = driver.find_element(By.NAME, 'quantity')
        edit_quantity_2 = driver.find_element(By.NAME, 'edit_quantity_button')

        # Change quantity of the food item to 101
        quantity_2_input.send_keys('101')
        edit_quantity_2.send_keys(Keys.RETURN)

        time.sleep(1)

        # Check that the user was not redirected
        edit_quantity_url_length = 46 + len(str(food_id))
        assert driver.current_url[:edit_quantity_url_length] == 'http://127.0.0.1:8000/user/shopping_cart/edit/{}'.format(food_id)

        # Check that some error message is displayed
        self.assertTrue("ERROR: New quantity must be less than 101." in driver.page_source, 
                        "Error message was not displayed")

        # check that quantity was not updated
        driver.get('http://127.0.0.1:8000/user/shopping_cart')
        self.assertTrue('Quantity: 1' in driver.page_source, 
                        "Shopping cart was updated with invalid Quantity form entry")
        
        # Remove food from cart so that it does not affect other test cases
        remove_food = driver.find_element(By.NAME, 'remove_food_button')
        remove_food.click()

    def test_delete_item(self):
        """
        Test if the item is removed form the cart when the 
        Remove button associated with the item is pressed

        Input:
        None
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to food page
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Add 1 item to the user's cart
        quantity_input.send_keys('1')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Delete the item
        remove_food = driver.find_element(By.NAME, 'remove_food_button')
        remove_food.click()

        time.sleep(1)

        # Verify that food 1 (Apple) has been removed from display
        assert 'Item: Apple' not in driver.page_source
        assert 'Restaurant: Fruit Market' not in driver.page_source
        assert 'Price per item: $1.000000' not in driver.page_source
        assert 'Quantity: 1' not in driver.page_source        

    def test_checkout_empty(self):
        """
        Case where the checkout button is pressed with an empty shopping cart

        Input:
        None
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to shopping cart page
        shopping_cart = driver.find_element(By.NAME, 'shopping_cart_button')
        shopping_cart.click()

        time.sleep(1)

        # Select checkout button
        checkout = driver.find_element(By.NAME, 'checkout_button')
        checkout.click()

        # Check that the user was not redirected
        assert driver.current_url == 'http://127.0.0.1:8000/user/shopping_cart/'

        # Check that some error message is displayed
        self.assertTrue("" in driver.page_source, 
                        "Error message was not displayed")

        # check that quantity was not updated
        driver.get('http://127.0.0.1:8000/user/view_orders')
        links = driver.find_elements(By.TAG_NAME, 'a')
        self.assertTrue(len(links) == 1, "An order was created")

    def test_checkout_empty(self):
        """
        Case where the checkout button is pressed with an empty shopping cart

        Input:
        None
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to shopping cart page
        shopping_cart = driver.find_element(By.NAME, 'shopping_cart_button')
        shopping_cart.click()

        time.sleep(1)

        # Select checkout button
        checkout = driver.find_element(By.NAME, 'checkout_button')
        checkout.click()

        # Check that the user was not redirected
        self.assertTrue(driver.current_url == 'http://127.0.0.1:8000/user/shopping_cart/',
                    "user was redirected")

        # Check that some error message is displayed
        self.assertTrue("ERROR: Shopping cart is empty." in driver.page_source, 
                        "Error message was not displayed")

        # check that quantity was not updated
        driver.get('http://127.0.0.1:8000/user/view_orders')
        links = driver.find_elements(By.TAG_NAME, 'a')
        self.assertTrue(len(links) == 1, "An order was created")

    def test_checkout_valid(self):
        """
        Case where the checkout button is pressed with a non-empty shopping cart

        Input:
        [{"Item": "Apple", "Restaurant": "Fruit Market", "Price": 1.000000, "Quantity": 5 }]
        """
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/user_stuff/login/')

        time.sleep(1)

        # Login
        email_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
       
        email_input.send_keys('test_user@gmail.com')
        password_input.send_keys('IAmAUs3r')

        login_button.send_keys(Keys.RETURN)
        
        time.sleep(1)

        # Navigate to food page
        driver.get('http://127.0.0.1:8000/user/restaurant/1/Fruits/Apple')
        quantity_input = driver.find_element(By.NAME, 'quantity')
        add_to_cart = driver.find_element(By.NAME, 'add_to_cart_button')

        # Add 1 item to the user's cart
        quantity_input.send_keys('1')
        add_to_cart.send_keys(Keys.RETURN)

        time.sleep(1)

        # Select checkout button
        checkout = driver.find_element(By.NAME, 'checkout_button')
        checkout.click()

        time.sleep(1)
        
        # Check that the user was redirected
        self.assertTrue(driver.current_url == 'http://127.0.0.1:8000/user/view_orders',
                    "user was not redirected")

        # check that an order appeared in the view orders page
        links = driver.find_elements(By.TAG_NAME, 'a')
        self.assertTrue(len(links) > 1, "An order was not created")