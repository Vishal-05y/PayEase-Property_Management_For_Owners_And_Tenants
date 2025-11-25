from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def tenantHome(request):
    return render(request, 'tenant/tenantHome.html')

def loginTenant(request):
    return render(request, 'tenant/loginTenant.html')