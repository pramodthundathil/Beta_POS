from django.shortcuts import render, redirect
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unautenticated_user

# Create your views here.
def Index(request):
    return render(request,"index.html")


@unautenticated_user
def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('Index')
        
        else:
            messages.error(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")


def SignOut(request):
    logout(request)
    return redirect('SignIn')