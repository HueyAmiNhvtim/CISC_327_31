from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AccountViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword',
            is_res_owner=False
        )

    def test_register_view(self):
        # White Box Testing Method: Decision Coverage Testing
        # Test 1: request.method is not 'POST'
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

        # Test 2: request.method is 'POST'
        response = self.client.post(reverse('accounts:register'), {'username': 'testuser', 'password1': 'testpassword1', 'password2': 'testpassword'})
        self.assertEqual(response.status_code, 200)

    def test_user_home_page_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(reverse('accounts:home_page'))
        self.assertEqual(response.status_code, 200)

    def test_res_owner_home_page_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(reverse('accounts:home_page'))
        self.assertEqual(response.status_code, 200)

    def test_edit_user_view(self):
        # White Box Testing Method: Path Testing

        self.client.login(email='test@example.com', password='testpassword')
        # Test 1: request.method is not 'POST'
        response = self.client.get(reverse('accounts:edit_user'))
        self.assertEqual(response.status_code, 200)

        # Test 2: request.method is 'POST', form is not valid
        response = self.client.post(reverse('accounts:edit_user'), {'username': 'testuser'})
        self.assertEqual(response.status_code, 200)

        # Test 3: request.method is 'POST', form is valid
        response = self.client.post(reverse('accounts:edit_user'), {'username': 'testuser2', 'email': 'test2@example.com'})
        self.assertEqual(response.status_code, 302)

    def test_password_change_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.post(reverse('accounts:change_password', kwargs={'user_id': self.user.id}), data={'user_id': self.user.id})
        self.assertEqual(response.status_code, 200)
