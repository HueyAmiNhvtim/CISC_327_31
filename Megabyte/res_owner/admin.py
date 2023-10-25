from django.contrib import admin

# Register your models here.
from .models import Restaurant, Food, Category

admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(Category)