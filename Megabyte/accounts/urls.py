from django.urls import path, include
from django.contrib.auth import urls
from . import views

app_name = 'accounts'
urlpatterns = [
    # Registration page,
    # Change ellis to something else......
    path('', views.welcome, name='ellis'),
    path('user_stuff/', include(urls)),  # Hopefully this will show the login page first...
    path('register/', views.register, name='register'),
    path('edit_user/<user_id>/', views.edit_user, name='edit_user'),
    # Home page for both user and res_owner
    path('home/<int:user_id>/', views.home_page, name='home_page'),
    # Home page for optional argument....
    path(r'^home/$', views.home_page, name='home_page')
]
