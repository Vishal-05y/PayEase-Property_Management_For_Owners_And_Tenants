from django.shortcuts import render, redirect
from .forms import TenantForm

# Create your views here.
def tenantHome(request):
    return render(request, 'tenant/tenantHome.html')


def loginTenant(request):
    return render(request, 'tenant/loginTenant.html')


def addTenant(request, flat_id):
    if request.method == "POST":
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('buildingsList')  # or ownerHome
    else:
        form = TenantForm()

    return render(request, 'tenant/addTenant.html', {'form': form})
