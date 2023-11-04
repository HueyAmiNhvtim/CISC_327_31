from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    # User home page
    path('', views.user_home_page, name='user_home_page'),
    # Search page
    path('search', views.search, name='search'),
    # Search results page
    path('search_results/', views.search_results, name='search_results'),
    # Restaurant page
    path('restaurant/<int:restaurant_id>', views.restaurant, name='restaurant'),
    # Category page
    path('restaurant/<int:restaurant_id>/<str:category_name>',
         views.category, name='category'),
    # Food page
    path('restaurant/<int:restaurant_id>/<str:category_name>/<str:food_name>',
         views.food, name='food'),
    # Add to shopping cart page
    path('shopping_cart/add/<int:restaurant_id>/<str:category_name>/<int:food_id>',
         views.add_to_shopping_cart, name='add_to_shopping_cart'),
    # Shopping cart page
    path('shopping_cart/',
         views.shopping_cart, name='shopping_cart'),
    # Change item quantity page
    path('shopping_cart/edit/<int:food_id>',
         views.edit_quantity, name='edit_quantity'),
    # Remove food from shopping cart page
    path('shopping_cart/remove/<int:food_id>',
         views.remove_food, name='remove_food'),
    # Checkout page
    path('checkout/', views.checkout, name='checkout'),
    # Order status page
    path('view_orders', views.view_orders, name='view_orders'),
    # Order details page
    path('view_orders/<int:order_id>', views.order, name='order'),


]
