import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

class RegistTest(LiveServerTestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--enable-features=NetworkService")
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.maximize_window()  #
    
    def tearDown(self):
        time.sleep(3)
        self.driver.quit()

    def test_regist_01_user(self):
        # user regist
        browser = self.driver
        browser.find_element(By.LINK_TEXT, 'Register').click()
        browser.find_element(By.NAME, 'email').send_keys('test111@123.com')
        browser.find_element(By.NAME, 'username').send_keys('test111')
        browser.find_element(By.NAME, 'password1').send_keys('testpassword')
        browser.find_element(By.NAME, 'password2').send_keys('testpassword')        
        browser.find_element(By.NAME, 'submit').click()
        # check result
        self.assertEqual(browser.current_url, 'http://127.0.0.1:8000/user/') 


    def test_regist_02_res_owner(self):
        # res owner regist
        browser = self.driver
        browser.find_element(By.LINK_TEXT, 'Register').click()
        browser.find_element(By.NAME, 'email').send_keys('test222@123.com')
        browser.find_element(By.NAME, 'username').send_keys('test222')
        browser.find_element(By.NAME, 'is_res_owner').click()
        browser.find_element(By.NAME, 'password1').send_keys('testpassword')
        browser.find_element(By.NAME, 'password2').send_keys('testpassword')
        browser.find_element(By.NAME, 'submit').click()
        # check result
        result = browser.find_elements(By.NAME, 'res_settings_button')
        self.assertTrue(len(result), 1)

    def test_regist_03_failure(self):
        # failure case
        browser = self.driver
        browser.find_element(By.LINK_TEXT, 'Register').click()
        browser.find_element(By.NAME, 'email').send_keys('test111@123.com')
        browser.find_element(By.NAME, 'username').send_keys('test111')
        browser.find_element(By.NAME, 'password1').send_keys('testpassword')
        browser.find_element(By.NAME, 'password2').send_keys('testpassword')        
        browser.find_element(By.NAME, 'submit').click()
        # check result        
        self.assertEqual(browser.current_url, 'http://127.0.0.1:8000/register/')  # failure regist, the current url still is 'http://127.0.0.1:8000/register/'
        


