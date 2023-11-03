from django.urls import path, include
from django.contrib.auth import urls
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    # Registration page,
    # Change ellis to something else......
    path('', views.welcome, name='ellis'),
    path('user_stuff/', include(urls)),  # Hopefully this will show the login page first...
    # Home page for both user and res_owner
    path('home/', views.home_page, name='home_page'),
    path('register/', views.register, name='register'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('<int:user_id>/password/',
         views.PasswordsChangeView.as_view(template_name='registration/change_password.html'),
         name='change_password'),
]
