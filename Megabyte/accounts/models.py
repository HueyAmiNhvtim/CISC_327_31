from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _   # For internationalization apparently
from django.utils import timezone
from ..res_owner.models import Restaurant
from django.db import models

from managers import CustomUserManager
from ..user.models import UserData, Quantity, ShoppingCart, Location, Order
# Create your models here.


class CustomUser(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=200)  # User can go by their name too
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_res_owner = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now())

    USERNAME_FIELDS = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['email', 'password']  # For the createsuperuser really.

    objects = CustomUserManager()  # Use the custom user manager for this custom user class
    # No need for password as that is already covered by the AbstractBaseUser class



