from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from members.forms import RegisterUser

# Create your views here.
def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "login Failed")
                return redirect('login')
        else:
            return render(request, 'members/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "logout successfull")
    return redirect('/')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = RegisterUser(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, 'Registration successfull')
                return redirect('/')
            else:
                messages.error(request, 'Registration failed')
                return redirect('register_user')
        else:
            form = RegisterUser()
            return render(request, 'members/register_user.html', {'form':form})
