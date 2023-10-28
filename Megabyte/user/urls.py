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
    # Search results page
    path('search_results/', views.search_results, name='search_results'),
    # Restaurant page
    path('restaurant/<int:restaurant_id>', views.restaurant, name='restaurant'),
    # Category page
    path('category/<str:category_name>', views.category, name='category'),
    # Food page
    path('food/<str:food_name>', views.food, name='food'),
    # Shopping cart page
    path('shopping_cart/',
         views.shopping_cart, name='shopping_cart'),
    # Order status page
    path('view_orders', views.view_orders, name='view_orders'),
    # Order details page
    path('order/<int:order_id>', views.order, name='order'),


]
