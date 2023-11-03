from django.test import TestCase
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationFormTest(TestCase):
    def test_custom_user_creation_form_valid_data(self):
        form = CustomUserCreationForm(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'is_res_owner': False
        })
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_invalid_data(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

class CustomUserChangeFormTest(TestCase):
    def test_custom_user_change_form_valid_data(self):
        user = get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        form = CustomUserChangeForm(instance=user, data={
            'email': 'test@example.com',
            'username': 'newusername',
            'password': 'newpassword'
        })
        self.assertTrue(form.is_valid())

    def test_custom_user_change_form_invalid_data(self):
        user = get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        form = CustomUserChangeForm(instance=user, data={'email': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
