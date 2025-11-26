from django.shortcuts import render
from .models import Tenant
from django.shortcuts import get_object_or_404

# Create your views here.

def ownerHome(request):
    tenants = Tenant.objects.all()
    return render(request, 'owner/ownerHome.html', {'tenants':tenants})

def loginOwner(request):
    return render(request, 'owner/loginOwner.html')

def tenantDetails(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    return render(request, 'owner/tenant_details.html', {'tenant':tenant})