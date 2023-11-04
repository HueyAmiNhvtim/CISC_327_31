from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# For internationalization apparently
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    # SHOULD TURN THIS TO TRUE BACK
    username = models.CharField(max_length=200, unique=False)
    # User can go by their name too
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_res_owner = models.BooleanField(default=False)

    # User's shopping cart
    cart = models.JSONField(default=list)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['username']  # For the createsuperuser really.

    # Use the custom user manager for this custom user class
    objects = CustomUserManager()
    # No need for password as that is already covered by the AbstractBaseUser class
