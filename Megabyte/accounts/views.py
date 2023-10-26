from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
# Create your views here.


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
            new_user = form.save(commit=False)
            login(request, new_user)   # Might have to be changed since we're using
                                       # custom User class
            if new_user.is_res_owner is True:
                return redirect('res_owner:res_home_page')
            else:
                return redirect('user:user_home_page')
    context = {'form': form}
    # if is_res_owner, send straight to restaurant_owner one
    # if user, send to the user equivalent.
    return render(request, 'accounts/register.html', context)


@login_required
def edit_user(request, user_id):
    """
    Edit the user's info
    :param request: a HttpRequest object specific to Django
    :param user_id: the id of the user. Should be unique too I think
    """
    this_user = CustomUser.objects.get(id=user_id)
    # Check to make sure if user cannot edit other user profile
    if this_user != request.user:
        raise Http404
    if request.method != 'POST':
        # Display the filled in registration form
        form = CustomUserChangeForm(instance=this_user)
    else:
        # POST data received. Process completed form
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            form.save()
            # if is_res_owner, send straight to restaurant_owner home page
            # if user, send to the user equivalent.
            if this_user.is_res_owner is True:
                return redirect('res_owner:res_home_page')
            else:
                return redirect('user:user_home_page')
    context = {'form': form}
    return render(request, 'accounts/edit_user.html', context)

