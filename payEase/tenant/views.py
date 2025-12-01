from django.shortcuts import render, redirect, get_object_or_404
from .forms import loginTenantForm
from .models import Tenant, RentPayment
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
def tenantHome(request):
    return render(request, 'tenant/tenantHome.html')


def loginTenant(request):
    if request.method == 'POST':
        form = loginTenantForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']

            # Get latest tenant entry for this person
            tenant = Tenant.objects.filter(name=name, phone=phone).order_by('-date_added').first()

            if tenant:
                # Store phone in session
                request.session['tenant_phone'] = phone

                # Instead of going to dashboard → check due first
                return redirect('tenantCheckDue')

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




def payRent(request):
    phone = request.session.get('tenant_phone')
    if not phone:
        return redirect('loginTenant')

    tenant = Tenant.objects.filter(phone=phone).order_by('-date_added').first()
    if not tenant:
        return HttpResponse("Tenant not found")

    current_month = datetime.now().strftime("%B %Y")

    already_paid = RentPayment.objects.filter(
        tenant=tenant,
        month=current_month,
        status="PAID"
    ).exists()

    return render(request, 'tenant/payRent.html', {
        'tenant': tenant,
        'current_month': current_month,
        'already_paid': already_paid
    })


def processPayment(request):
    if request.method != "POST":
        return redirect('tenantDashboard')

    phone = request.session.get('tenant_phone')
    tenant = Tenant.objects.filter(phone=phone).order_by('-date_added').first()
    if not tenant:
        return HttpResponse("Tenant not found")

    current_month = datetime.now().strftime("%B %Y")

    # prevent duplicate payment
    if RentPayment.objects.filter(tenant=tenant, month=current_month, status="PAID").exists():
        return redirect('paymentSuccess')

    fake_payment_id = f"FAKEPAY-{datetime.now().timestamp()}"

    RentPayment.objects.create(
        tenant=tenant,
        flat=tenant.flat,
        amount=tenant.flat_price,
        month=current_month,
        status="PAID",
        payment_id=fake_payment_id
    )

    return redirect('paymentSuccess')



def paymentSuccess(request):
    phone = request.session.get('tenant_phone')
    tenant = Tenant.objects.filter(phone=phone).order_by('-date_added').first()

    last_payment = RentPayment.objects.filter(
        tenant=tenant
    ).order_by('-date_paid').first()

    return render(request, 'tenant/paymentSuccess.html', {
        'tenant': tenant,
        'payment': last_payment
    })


def rentHistory(request):
    phone = request.session.get('tenant_phone')
    tenant = Tenant.objects.filter(phone=phone).order_by('-date_added').first()

    payments = RentPayment.objects.filter(
        tenant=tenant
    ).order_by('-id')

    return render(request, 'tenant/rentHistory.html', {
        'tenant': tenant,
        'payments': payments
    })


def logoutTenant(request):
    request.session.flush()
    return redirect('loginTenant')



def tenantCheckDue(request):
    phone = request.session.get('tenant_phone')
    if not phone:
        return redirect('loginTenant')

    # latest tenant
    tenant = Tenant.objects.filter(phone=phone).order_by('-date_added').first()

    if not tenant:
        return HttpResponse("Tenant not found")

    # current month
    current_month = datetime.now().strftime("%B %Y")

    # has he paid?
    paid = RentPayment.objects.filter(
        tenant=tenant,
        month=current_month,
        status="PAID"
    ).exists()

    if paid:
        return redirect('tenantDashboard')

    # show due alert
    return render(request, "tenant/rentDuePrompt.html", {
        "tenant": tenant,
        "current_month": current_month
    })
