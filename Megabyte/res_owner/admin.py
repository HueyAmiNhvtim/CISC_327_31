from django.contrib import admin

# Register your models here.
from .models import RestaurantOwner, Restaurant, Food

admin.site.register(RestaurantOwner)
admin.site.register(Restaurant)
admin.site.register(Food)
