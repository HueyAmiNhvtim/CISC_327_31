from django.urls import path, include
# from django.contrib.auth import urls
from . import views

app_name = 'accounts'
urlpatterns = [
    # Registration page,
    path('', views.register, name='register'),
    path('edit_user/<user_id>', views.edit_user, name='edit_user'),
    # Home page
    path('home/<int:user_id>', views.home_page, name='home_page')
]
