from django.urls import path, include
from django.contrib.auth import urls
from . import views

app_name = 'accounts'
urlpatterns = [
    # Include default urls
    path('', include(urls)),
    # Registration page,
    path('register/', views.register, name='register'),
    path('edit_user/<email>', views.edit_user, name='edit_user')
]
