from django.contrib import admin

# Register your models here.
from users import models
admin.site.register(models.UserInfo)
admin.site.register(models.OwnerInfo)
