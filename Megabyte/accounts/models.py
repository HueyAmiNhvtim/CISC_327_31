from django.db import models
from ..res_owner.models import Restaurant
from ..user.models import UserData, Quantity, ShoppingCart, Location, Order
# Create your models here.


class GeneralUser(models.Model):
    pass


class UserExclusive(models.Model):
    pass


class ResOwnerExclusive(models.Model):
    pass


