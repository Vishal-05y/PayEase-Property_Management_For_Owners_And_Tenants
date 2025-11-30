from django.shortcuts import render, redirect, get_object_or_404
from .forms import addTenantForm, loginTenantForm
from owner.models import Flat
from django.utils import timezone
from .models import Tenant
from django.http import HttpResponse

# Create your views here.
def tenantHome(request):
    return render(request, 'tenant/tenantHome.html')


def loginTenant(request):
    if request.method == 'POST':
        form = loginTenantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']

            # Get all tenant records with this phone
            tenants = Tenant.objects.filter(name=name, phone=phone).order_by('-date_added')

            if tenants.exists():
                return redirect('tenantDashboard', phone=phone)
            else:
                return render(request, 'tenant/loginTenant.html', {
                    'form': form,
                    'error': "No tenant found with this phone number."
                })
    else:
        form = loginTenantForm()

    return render(request, 'tenant/loginTenant.html', {'form': form})


def tenantDashboard(request, phone):
    # Get all flat records for this phone
    tenant = Tenant.objects.filter(phone=phone).select_related('flat', 'flat__building').order_by('-date_added')

    if not tenant.exists():
        return HttpResponse("No tenant found with this phone number")
    
    latest_flat = tenant.first()

    return render(request, 'tenant/tenantDashboard.html', {
        'tenant': latest_flat,
        'phone': phone,
    })


def addTenant(request, phone, building_id, flat_id):
    flat = get_object_or_404(Flat, id=flat_id, building_id=building_id)

    if request.method == "POST":
        form = addTenantForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            tphone = form.cleaned_data['phone']
            flat_price = form.cleaned_data['flat_price']

            # Check if same tenant existed before in this flat
            try:
                existing_tenant = Tenant.objects.get(flat=flat, phone=tphone)

                # If tenant is rejoining, update instead of new record
                existing_tenant.name = name
                existing_tenant.flat_price = flat_price
                existing_tenant.date_added = timezone.now()
                existing_tenant.save()

                return redirect('flatDetails', phone, building_id, flat_id)

            except Tenant.DoesNotExist:
                # If no previous tenant, create new
                tenant = form.save(commit=False)
                tenant.flat = flat
                tenant.save()

                return redirect('flatDetails', phone, building_id, flat_id)
    
    else:
        form = addTenantForm()

    return render(request, 'tenant/addTenant.html', {
        'form': form,
        'flat': flat
    })


def allFlats(request, phone):
    # Get all flat records for this phone
    tenant = Tenant.objects.filter(phone=phone).select_related('flat', 'flat__building').order_by('-date_added')

    if not tenant.exists():
        return HttpResponse("No tenant found with this phone number")

    return render(request, 'tenant/allFlats.html', {
        'tenant': tenant,
        'phone': phone,
    })
