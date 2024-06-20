from django.shortcuts import render, redirect

# Create your views here.

def POS(request):
    return render(request,'pos.html')
