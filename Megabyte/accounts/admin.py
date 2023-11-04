from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Fields to be used in displaying the User model in the Admin page
    list_display = ['email', 'username', 'is_res_owner', 'is_staff', 'is_active']
    list_filter = ['email', 'username', 'is_res_owner', 'is_staff', 'is_active']
    fieldsets = [
        (None, {'fields': ('email', 'password', 'username', 'is_res_owner')}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    ]
    # add_fieldsets allows for the custom UserAdmin to use this attribute when
    # creating a user
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password1', 'password2', 'is_res_owner',
                'is_staff', 'groups', 'user_permissions'
            )
        }
        )
    ]
    search_fields = ('email', 'username')
    ordering = ('email', 'username')


admin.site.register(CustomUser, CustomUserAdmin)