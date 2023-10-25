from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomUserChangeForm

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
            # Get the boolean value of whether they choose the res_owner or not here....
    context = {'form': form}
    # if is_res_owner, send straight to restaurant_owner one
    # if user, send to the user equivalent.
    return render(request, 'accounts/register.html', context)


def edit_user(request):
    """
    Edit the user's info
    :param request: a HttpRequest object specific to Django
    """
    pass

