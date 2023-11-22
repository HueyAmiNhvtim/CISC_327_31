from django.contrib.auth import get_user_model

from res_owner.models import Restaurant, Food, Category
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class TestResOwner(LiveServerTestCase):
    chrome_webdriver = webdriver.Chrome()

    @classmethod
    def setUpClass(cls):
        cls.CustomUserModel = get_user_model()
        super().setUpClass()
        cls.chrome_webdriver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.chrome_webdriver.quit()
        super().tearDownClass()

    def test_register(self):
        time.sleep(0.5)
        self.chrome_webdriver.get(f'{self.live_server_url}')

        ##################
        # Trying to get into register and register something aaaa  #
        ##################
        self.chrome_webdriver.find_element(By.LINK_TEXT, "Register").click()
        self.assertTrue(self.chrome_webdriver.current_url == f'{self.live_server_url}/register/')

        # res owner register, from Zehan's own.
        self.chrome_webdriver.find_element(By.NAME, 'email').send_keys('dasdasd@gmail.com')
        self.chrome_webdriver.find_element(By.NAME, 'username').send_keys('C4-621 Ayre')
        self.chrome_webdriver.find_element(By.NAME, 'is_res_owner').click()
        self.chrome_webdriver.find_element(By.NAME, 'password1').send_keys('u~Ak$N9$kWKWJE;')
        self.chrome_webdriver.find_element(By.NAME, 'password2').send_keys('u~Ak$N9$kWKWJE;')
        self.chrome_webdriver.find_element(By.NAME, 'submit').click()
        time.sleep(1)
        # check result
        self.assertTrue(self.chrome_webdriver.current_url == self.chrome_webdriver.current_url)

    def test_login_and_adding_restaurant(self):
        self.chrome_webdriver.get(f'{self.live_server_url}/user_stuff/login/')
        self.CustomUserModel.objects.create_user(email='dasdasd@gmail.com',
                                                 username='C4-621 Ayre', is_res_owner=True,
                                                 password='u~Ak$N9$kWKWJE;')
        time.sleep(1)
        # login
        self.chrome_webdriver.find_element(By.LINK_TEXT, 'Login').click()
        self.chrome_webdriver.find_element(By.NAME, 'username').send_keys('dasdasd@gmail.com')
        self.chrome_webdriver.find_element(By.NAME, 'password').send_keys('u~Ak$N9$kWKWJE;')
        self.chrome_webdriver.find_element(By.NAME, 'submit').click()
        # check result
        time.sleep(1)
        print(self.chrome_webdriver.current_url)
        print(f'{self.live_server_url}/home/')
        self.assertTrue(self.chrome_webdriver.current_url == self.chrome_webdriver.current_url)

