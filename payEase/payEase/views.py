from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Hi")

def loginOwner(request):
    return render(request, 'loginOwner.html')

def loginTenant(request):
    return render(request, 'loginTenant.html')