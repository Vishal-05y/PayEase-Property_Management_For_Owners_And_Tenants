from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def ownerHome(request):
    return HttpResponse('Hi Owner')

def loginOwner(request):
    return render(request, 'loginOwner.html')