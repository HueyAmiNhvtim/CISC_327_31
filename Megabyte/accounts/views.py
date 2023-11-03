from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.http import Http404

from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser
from django.urls import reverse_lazy
from res_owner.models import Restaurant
# Do same thing for User later.

# Create your views here.


class PasswordsChangeView(PasswordChangeView):
    """Custom password change view"""
    form_class = PasswordChangeForm
    # Go to the home_page URLs in the urls.py of this app once password changing is done
    success_url = reverse_lazy(viewname='accounts:home_page')


def register(request):
    """
    Register a new user
    :param request: a HttpRequest object specific to Django
    """
    if request.method != 'POST':
        # Display the blank registration form
        form = CustomUserCreationForm()
    else:
        # POST data received. Process completed form
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)  # Might have to be changed since we're using
            # custom User class
            if new_user.is_res_owner is True:
                return redirect('res_owner:res_home_page', user_id=new_user.id)
            else:
                return redirect('user:user_home_page')
    context = {'form': form}
    # if is_res_owner, send straight to restaurant_owner one
    # if user, send to the user equivalent.
    return render(request, 'registration/register.html', context)


@login_required
def edit_user(request):
    """
    Edit the user's info
    :param request: a HttpRequest object specific to Django
    """
    if request.method != 'POST':
        # Display the filled in registration form
        form = CustomUserChangeForm(instance=request.user)
    else:
        # POST data received. Process completed form
        form = CustomUserChangeForm(instance=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            # if is_res_owner, send straight to restaurant_owner home page
            # if user, send to the user equivalent. 
            if request.user.is_res_owner is True:
                return redirect('res_owner:res_home_page', user_id=request.user.id)
            else:
                return redirect('user:user_home_page')
    context = {'form': form}
    return render(request, 'registration/edit_user.html', context)


def home_page(request):
    """
    Edit the user's info
    :param request: a HttpRequest object specific to Django
    """
    # No user => Redirect to the welcome one
    if request.user.is_anonymous:
        return redirect('accounts:ellis')
    if request.user.is_res_owner is True:
        restaurants = Restaurant.objects.filter(restaurant_owner=request.user).order_by('name')
        context = {'restaurants': restaurants, 'user_id': request.user.id, 'email': request.user.email}
        return render(request, 'res_owner/res_home_page.html', context)
    else:
        return render(request, 'user/user_home_page.html')


def welcome(request):
    """
    Simple views function for the welcome page
    """
    return render(request, 'registration/welcome.html')
