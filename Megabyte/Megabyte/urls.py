"""
URL configuration for Megabyte project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Always add new apps here if you haven't already.
    # Probably gonna make the default page to be the accounts page,
    # and in the accounts page, the default url is the login page. muahahahaah
    path('admin/', admin.site.urls),
    # I'm not too sure about this...Should we have a separate home page to show different
    # pages for different kinds of users using the same URL?
    path('', include('accounts.urls')),
    path('res_owner/', include('res_owner.urls')),
    path('user/', include('user.urls')),
]
