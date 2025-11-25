from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def tenantHome(request):
    return HttpResponse('Hi Tenant')

def loginTenant(request):
    return render(request, 'loginTenant.html')