import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

class EditInfoTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.maximize_window()  #
    
    def tearDown(self):
        time.sleep(3)
        self.driver.quit()

    def test_01_edit_info(self):
        browser = self.driver
        # login
        browser.find_element(By.LINK_TEXT, 'Login').click()
        browser.find_element(By.NAME, 'username').send_keys('test111@123.com')
        browser.find_element(By.NAME, 'password').send_keys('testpassword')
        browser.find_element(By.NAME, 'submit').click()
        browser.find_element(By.XPATH, '/html/body/form[6]/button').click()
        # edit info
        browser.find_element(By.NAME, 'username').clear()
        browser.find_element(By.NAME, 'username').send_keys('test12')
        browser.find_element(By.NAME, 'email').clear()
        browser.find_element(By.NAME, 'email').send_keys('test12@123.com')
        browser.find_element(By.NAME, 'submit').click()
        # check result
        result = browser.find_elements(By.NAME, 'user_settings_button')
        self.assertTrue(len(result), 1)

    def test_02_change_password(self):
        browser = self.driver
        # login
        browser.find_element(By.LINK_TEXT, 'Login').click()
        browser.find_element(By.NAME, 'username').send_keys('test12@123.com')
        browser.find_element(By.NAME, 'password').send_keys('testpassword')
        browser.find_element(By.NAME, 'submit').click()
        browser.find_element(By.XPATH, '/html/body/form[6]/button').click()
        browser.find_element(By.LINK_TEXT, 'this form').click()
        # change password
        browser.find_element(By.NAME, 'old_password').send_keys('testpassword')
        browser.find_element(By.NAME, 'new_password1').send_keys('tt12pwd123')
        browser.find_element(By.NAME, 'new_password2').send_keys('tt12pwd123')
        browser.find_element(By.NAME, 'submit').click()
        # check result
        result = browser.find_elements(By.NAME, 'user_settings_button')
        self.assertTrue(len(result), 1)




        


