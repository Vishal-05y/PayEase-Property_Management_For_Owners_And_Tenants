from django.shortcuts import render, redirect, get_object_or_404
from .forms import loginTenantForm
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

            tenant = Tenant.objects.filter(name=name, phone=phone).order_by('-date_added').first()

            if tenant:
                request.session['tenant_phone'] = phone
                return redirect('tenantDashboard')

            return render(request, 'tenant/loginTenant.html', {
                'form': form,
                'error': "You are not registered yet. Please contact your owner."
            })

    else:
        form = loginTenantForm()

    return render(request, 'tenant/loginTenant.html', {
        'form': form
    })


def tenantDashboard(request):
    phone = request.session.get('tenant_phone')

    if not phone:
        return redirect('loginTenant')

    tenants = Tenant.objects.filter(phone=phone).select_related('flat', 'flat__building').order_by('-date_added')

    if not tenants.exists():
        return HttpResponse("Tenant not found")

    latest_flat = tenants.first()

    return render(request, 'tenant/tenantDashboard.html', {
        'tenant': latest_flat,
    })


def allFlats(request):
    phone = request.session.get('tenant_phone')

    if not phone:
        return redirect('loginTenant')

    tenants = Tenant.objects.filter(phone=phone).select_related('flat', 'flat__building').order_by('-date_added')

    return render(request, 'tenant/allFlats.html', {
        'tenant': tenants,
    })


def logoutTenant(request):
    request.session.flush()
    return redirect('loginTenant')
