from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager.
    Unique identifier is the email rather than the usernames in the default one
    """

    def create_user(self, email, username, password, is_res_owner: bool = False, **extra_fields):
        """
        Create and save a user.
        The unique identifier of the user is their email.
        :param email: the email of user
        :param username: their username
        :param password: their password
        :param is_res_owner: the boolean indicating if they are a restaurant owner or not.
                             Default is False.
        :return: an instance of the user
        """
        if not email:
            raise ValueError(_('The email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, is_res_owner=is_res_owner, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create and save a SuperUser (basically the admin).
        The unique identifier of the user is their email.
        :param email: the email of user
        :param username: their username
        :param password: their password
        :return: an instance of the user
        """
        # Set fields for the admin if those fields don't exist in extra_fields
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_res_owner', True)  # Admin can be res_owner for debugging purposes
        extra_fields.setdefault('username', username)

        # Check if existing fields in extra_fields violate what makes an admin
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('SuperUser must have is_staff = True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('SuperUser must have is_superuser = True'))
        if extra_fields.get('is_res_owner') is not True:
            raise ValueError(_('SuperUser must also be a restaurant owner for debugging purposes'))
        return self.create_user(email=email, password=password, **extra_fields)
