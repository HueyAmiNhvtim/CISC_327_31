from django.db import models

# Create your models here.

# user_info table
class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.EmailField()

# owner_info table
class OwnerInfo(models.Model):
    owner_name = models.CharField(max_length=32)    
    owner_password = models.CharField(max_length=32)
    owner_email = models.EmailField()
    restaurant_name = models.CharField(max_length=100)
    restaurant_location = models.CharField(max_length=200)
    restaurant_type = models.CharField(max_length=100)
    restaurant_description = models.CharField(max_length=200)
    proof = models.CharField(max_length=100)
