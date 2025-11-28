from django.shortcuts import render, redirect, get_object_or_404
from .forms import TenantForm
from owner.models import Flat
from django.db import IntegrityError

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
            tenant = form.save(commit=False)
            tenant.flat = flat
            try:
                tenant.save()
                return redirect('flatDetails', building_id=building_id, flat_id=flat_id)
            except IntegrityError:
                form.add_error("phone", "This phone number already exists.")
    else:
        form = TenantForm()

    return render(request, 'tenant/addTenant.html', {
        'form': form,
        'flat': flat
    })


# def tenantDetails(request, building_id, flat_id):
#     tenant = Tenant.objects.all()
#     return render(request, 'tenant/tenantDetails.html', {'tenant':tenant})