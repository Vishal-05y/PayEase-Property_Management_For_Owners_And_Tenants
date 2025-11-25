from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def ownerHome(request):
    return render(request, 'owner/ownerHome.html' )

def loginOwner(request):
    return render(request, 'owner/loginOwner.html')