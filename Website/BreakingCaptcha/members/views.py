from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from .forms import RegistrationUserForm


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You logged successfully.")
            return redirect('home')
        else:
            messages.error(
                request, "The username or password are not correct, please try again later.")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logout out!')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have been registered successfully ')
            return redirect('home')
    else:
        form = RegistrationUserForm
    return render(request, 'authenticate/register_user.html', {
        'form': form
    })


#def reset_user_password():
#    return 

#def reset_user_password_done():
#    return