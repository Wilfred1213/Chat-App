
from django.shortcuts import render, redirect
from authentications.forms import *

from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login,logout

# Create your views here.
def register_user(request):
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():   
            form.save() 
            return redirect('authentications:loggin')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentications/signup.html', {'form': form,})


def loggin(request):
    user_id = request.user
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user_id.is_online =True
                messages.info(request, 'Login successful')
                return redirect('index')           
            messages.info(request, 'Invalid data')
            return redirect('authentications:loggin')
    else:
        form = LoginForm(request)
    return render(request, 'authentications/signin.html', {'form': form,})

def logout(request):
    auth.logout(request)
    messages.success(request, 'You logout! Loging again?')
    return redirect('authentications:loggin')