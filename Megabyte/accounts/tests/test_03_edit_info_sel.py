import time
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

class EditInfoTest(LiveServerTestCase):
    def setUp(self):
        self.CustomUserModel = get_user_model()
        self.driver = webdriver.Chrome()
        self.driver.get(f'{self.live_server_url}')
        self.driver.maximize_window()  #

    def tearDown(self):
        time.sleep(3)
        self.driver.quit()

    def test_01_edit_info(self):
        browser = self.driver
        self.CustomUserModel.objects.create_user(email='testedit@123.com',
                                                 username='testedit', is_res_owner=False,
                                                 password='testpassword')
        # login
        browser.find_element(By.LINK_TEXT, 'Login').click()
        browser.find_element(By.NAME, 'username').send_keys('testedit@123.com')
        browser.find_element(By.NAME, 'password').send_keys('testpassword')
        browser.find_element(By.NAME, 'submit').click()
        browser.find_element(By.XPATH, '/html/body/form[5]/button').click()
        # edit info
        browser.find_element(By.NAME, 'username').clear()
        browser.find_element(By.NAME, 'username').send_keys('test12')
        browser.find_element(By.NAME, 'email').clear()
        browser.find_element(By.NAME, 'email').send_keys('test12@123.com')
        browser.find_element(By.NAME, 'submit').click()
        # check result
        result = browser.find_elements(By.NAME, 'search_button')
        self.assertTrue(len(result), 1)

    def test_02_change_password(self):
        browser = self.driver
        self.CustomUserModel.objects.create_user(email='testedit@123.com',
                                                 username='testedit', is_res_owner=False,
                                                 password='testpassword')
        # login
        browser.find_element(By.LINK_TEXT, 'Login').click()
        browser.find_element(By.NAME, 'username').send_keys('testedit@123.com')
        browser.find_element(By.NAME, 'password').send_keys('testpassword')
        browser.find_element(By.NAME, 'submit').click()
        browser.find_element(By.XPATH, '/html/body/form[5]/button').click()
        browser.find_element(By.LINK_TEXT, 'this form').click()
        # change password
        browser.find_element(By.NAME, 'old_password').send_keys('testpassword')
        browser.find_element(By.NAME, 'new_password1').send_keys('tt12pwd123')
        browser.find_element(By.NAME, 'new_password2').send_keys('tt12pwd123')
        browser.find_element(By.NAME, 'submit').click()
        # check result
        result = browser.find_elements(By.NAME, 'search_button')
        self.assertTrue(len(result), 1)




        


