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
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_user_home_page_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(reverse('accounts:home_page'))
        self.assertEqual(response.status_code, 200)

    def test_res_owner_home_page_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(reverse('accounts:home_page'))
        self.assertEqual(response.status_code, 200)

    def test_edit_user_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(reverse('accounts:edit_user'))
        self.assertEqual(response.status_code, 200)

    def test_password_change_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.post(reverse('accounts:change_password', kwargs={'user_id': self.user.id}), data={'user_id': self.user.id})
        self.assertEqual(response.status_code, 200)
