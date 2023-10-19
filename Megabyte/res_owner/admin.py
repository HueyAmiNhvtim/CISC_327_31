from django.contrib import admin

# Register your models here.
from .models import RestaurantOwner, Restaurant, Menu

admin.site.register(RestaurantOwner)
admin.site.register(Restaurant)
admin.site.register(Menu)
