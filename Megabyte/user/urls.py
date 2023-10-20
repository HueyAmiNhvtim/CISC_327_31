from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    # User home page
    path('', views.user_home_page, name='user_home_page'),
    # User settings to change user data
    path('user_settings/', views.user_settings, name='user_settings'),
    # Search page
    path('search', views.search, name='search'),
    # Restaurant page
    path('restaurant/<int:restaurant_id>', views.restaurant, name='restaurant'),
    # Shopping cart page
    path('shopping_cart/<int:user_id>',
         views.shopping_cart, name='shopping_cart'),
    # Order status page
    path('view_orders', views.view_orders, name='view_orders'),
    # Order details page
    path('order/<int:order_id>', views.order, name='order'),


]
