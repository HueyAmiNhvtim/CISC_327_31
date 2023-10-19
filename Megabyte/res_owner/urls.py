"""Define URL patterns for the res_owner sections"""
from django.urls import path
from . import views


app_name = 'res_owner'
urlpatterns = [
    # Home_page for restaurant owners
    path('', views.res_home_page, name='res_home_page')
]
