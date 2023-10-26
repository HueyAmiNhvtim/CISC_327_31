from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _   # For internationalization apparently
from django.utils import timezone
from django.db import models

from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=200, unique=False)  # SHOULD TURN THIS TO TRUE BACK
    # User can go by their name too
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_res_owner = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['username']  # For the createsuperuser really.

    objects = CustomUserManager()  # Use the custom user manager for this custom user class
    # No need for password as that is already covered by the AbstractBaseUser class



