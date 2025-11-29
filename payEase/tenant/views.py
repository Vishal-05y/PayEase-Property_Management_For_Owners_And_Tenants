from django.shortcuts import render, redirect, get_object_or_404
from .forms import TenantForm
from owner.models import Flat
from django.utils import timezone
from .models import Tenant

# Create your views here.
def tenantHome(request):
    return render(request, 'tenant/tenantHome.html')


def loginTenant(request):
    return render(request, 'tenant/loginTenant.html')


def addTenant(request, building_id, flat_id):
    flat = get_object_or_404(Flat, id=flat_id, building_id=building_id)

    if request.method == "POST":
        form = TenantForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            flat_price = form.cleaned_data['flat_price']

            # Check if same tenant existed before in this flat
            try:
                existing_tenant = Tenant.objects.get(flat=flat, phone=phone)

                # If tenant is rejoining, update instead of new record
                existing_tenant.name = name
                existing_tenant.flat_price = flat_price
                existing_tenant.date_added = timezone.now()
                existing_tenant.save()

                return redirect('flatDetails', building_id=building_id, flat_id=flat_id)

            except Tenant.DoesNotExist:
                # If no previous tenant, create new
                tenant = form.save(commit=False)
                tenant.flat = flat
                tenant.save()

                return redirect('flatDetails', building_id=building_id, flat_id=flat_id)
    
    else:
        form = TenantForm()

    return render(request, 'tenant/addTenant.html', {
        'form': form,
        'flat': flat
    })


# def tenantDetails(request, building_id, flat_id):
#     tenant = Tenant.objects.all()
#     return render(request, 'tenant/tenantDetails.html', {'tenant':tenant})