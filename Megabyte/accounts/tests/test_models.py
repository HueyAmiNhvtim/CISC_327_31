from django.test import TestCase
from accounts.models import CustomUser
from django.contrib.auth import get_user_model


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_res_owner)

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(
            email='admin@example.com',
            username='adminuser',
            password='adminpassword'
        )
        self.assertEqual(admin.username, 'adminuser')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_res_owner)
