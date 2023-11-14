import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.maximize_window()  #
    
    def tearDown(self):
        time.sleep(3)
        self.driver.quit()

    def test_login(self):
        browser = self.driver
        # login
        browser.find_element(By.LINK_TEXT, 'Login').click()
        browser.find_element(By.NAME, 'username').send_keys('test111@123.com')
        browser.find_element(By.NAME, 'password').send_keys('testpassword')
        browser.find_element(By.NAME, 'submit').click()
        # check result
        result = browser.find_elements(By.NAME, 'user_settings_button')
        self.assertTrue(len(result), 1)






