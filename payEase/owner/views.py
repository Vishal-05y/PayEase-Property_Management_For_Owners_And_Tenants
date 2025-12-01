from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import Owner, Building, Flat
from .forms import SignUpOwnerForm, LoginOwnerForm, BuildingForm, FlatForm, addTenantForm
from datetime import datetime

from tenant.models import Tenant, RentPayment

def ownerHome(request):
    return render(request, 'owner/ownerHome.html')


# -------------------- SIGNUP --------------------

def signUpOwner(request):
    if request.method == 'POST':
        form = SignUpOwnerForm(request.POST)

        if form.is_valid():
            phone = form.cleaned_data['phone']

            if Owner.objects.filter(phone=phone).exists():
                return render(request, 'owner/signUpOwner.html', {
                    'form': form,
                    'error': "Number already registered."
                })

            form.save()
            return redirect('loginOwner')

    else:
        form = SignUpOwnerForm()

    return render(request, 'owner/signUpOwner.html', {'form': form})


# -------------------- LOGIN --------------------

def loginOwner(request):
    if request.method == 'POST':
        form = LoginOwnerForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']

            owner = Owner.objects.filter(name=name, phone=phone).first()

            if owner:
                request.session['owner_phone'] = phone
                return redirect('ownerDashboard')

            return render(request, 'owner/loginOwner.html', {
                'form': form,
                'error': "You are not registered."
            })

    else:
        form = LoginOwnerForm()

    return render(request, 'owner/loginOwner.html', {'form': form})


# -------------------- LOGOUT --------------------

def logoutOwner(request):
    request.session.flush()
    return redirect('loginOwner')


# -------------------- DASHBOARD --------------------

def ownerDashboard(request):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    owner = Owner.objects.filter(phone=phone).first()
    if not owner:
        return HttpResponse("Owner not found")

    buildings = Building.objects.filter(owner=owner)
    flats = Flat.objects.filter(building__owner=owner)

    # Count only ACTIVE tenants
    occupied = Tenant.objects.filter(
        flat__building__owner=owner, 
        is_active=True
    ).values('flat').distinct().count()

    # Current month
    current_month = datetime.now().strftime("%B %Y")

    # Get all ACTIVE tenants only
    active_tenants = Tenant.objects.filter(
        flat__building__owner=owner,
        is_active=True
    ).order_by('flat_id', '-date_added')

    # Only 1 active tenant per flat → safe
    latest_active_tenants = {}
    for t in active_tenants:
        if t.flat_id not in latest_active_tenants:
            latest_active_tenants[t.flat_id] = t

    # Find unpaid tenants from ACTIVE ones
    unpaid_tenants = []
    for tenant in latest_active_tenants.values():
        paid = RentPayment.objects.filter(
            tenant=tenant,
            month=current_month,
            status="PAID"
        ).exists()

        if not paid:
            unpaid_tenants.append(tenant)

    return render(request, "owner/ownerDashboard.html", {
        "owner": owner,
        "buildings": buildings,
        "total_buildings": buildings.count(),
        "total_flats": flats.count(),

        # Only count active tenants
        "occupied_flats": occupied,
        "vacant_flats": flats.count() - occupied,

        # Show unpaid tenants for this month
        "unpaid_tenants": unpaid_tenants,
        "current_month": current_month,
    })


# -------------------- ADD BUILDING --------------------

def addBuilding(request):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    owner = get_object_or_404(Owner, phone=phone)

    if request.method == "POST":
        form = BuildingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']

            # Check for duplicate building for same owner
            if Building.objects.filter(owner=owner, name=name, address=address).exists():
                return render(request, 'building/addBuilding.html', {
                    'form': form,
                    'error': "Building already exists. Try adding flats in it or create a new building."
                })

            # Otherwise save building
            building = form.save(commit=False)
            building.owner = owner
            building.save()

            return redirect('ownerDashboard')

    else:
        form = BuildingForm()

    return render(request, 'building/addBuilding.html', {
        'form': form
    })


# -------------------- BUILDING DETAILS --------------------

def buildingDetails(request, building_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    # Get building owned by this owner
    building = get_object_or_404(Building, id=building_id, owner__phone=phone)

    flats = building.flats.all()
    current_month = datetime.now().strftime("%B %Y")

    unpaid_tenants = []

    for flat in flats:
        # Only ACTIVE tenant for this flat
        latest_tenant = flat.tenants.filter(is_active=True).order_by('-date_added').first()

        if latest_tenant:
            paid = RentPayment.objects.filter(
                tenant=latest_tenant,
                flat=flat,
                month=current_month,
                status="PAID"
            ).exists()

            if not paid:
                unpaid_tenants.append(latest_tenant)

    return render(request, 'building/buildingDetails.html', {
        'building': building,
        'flats': flats,
        'unpaid_tenants': unpaid_tenants,
        'current_month': current_month,
    })


# -------------------- ADD FLAT --------------------

def addFlat(request, building_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    building = get_object_or_404(Building, id=building_id, owner__phone=phone)

    if request.method == "POST":
        form = FlatForm(request.POST)
        if form.is_valid():
            flat_number = form.cleaned_data['flat_number']

            # Duplicate check for FLATS inside the SAME BUILDING
            if Flat.objects.filter(building=building, flat_number=flat_number).exists():
                return render(request, 'flat/addFlat.html', {
                    'form': form,
                    'building': building,
                    'error': "This flat number already exists in this building. Try to add a different flat number."
                })

            flat = form.save(commit=False)
            flat.building = building
            flat.save()

            return redirect('buildingDetails', building_id=building_id)

    else:
        form = FlatForm()

    return render(request, 'flat/addFlat.html', {
        'form': form,
        'building': building
    })


# -------------------- FLAT DETAILS --------------------

def flatDetails(request, building_id, flat_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    flat = get_object_or_404(
        Flat, 
        id=flat_id,
        building_id=building_id,
        building__owner__phone=phone
    )

    # Only ACTIVE tenant
    tenant = flat.tenants.filter(is_active=True).order_by('-date_added').first()

    return render(request, 'flat/flatDetails.html', {
        'flat': flat,
        'tenant': tenant,
    })


# -------------------- ADD TENANT --------------------

def addTenant(request, building_id, flat_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    flat = get_object_or_404(
        Flat,
        id=flat_id,
        building_id=building_id,
        building__owner__phone=phone
    )

    if request.method == "POST":
        form = addTenantForm(request.POST)

        if form.is_valid():
            # 1. Deactivate existing active tenant (if any)
            Tenant.objects.filter(flat=flat, is_active=True).update(is_active=False)

            # 2. Create new tenant as active
            tenant = form.save(commit=False)
            tenant.flat = flat
            tenant.is_active = True
            tenant.save()

            return redirect('flatDetails', building_id=building_id, flat_id=flat_id)

    else:
        form = addTenantForm()

    return render(request, 'tenant/addTenant.html', {
        'form': form,
        'flat': flat
    })


# -------------------- REMOVE TENANT --------------------

def removeTenant(request, building_id, flat_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    flat = get_object_or_404(
        Flat,
        id=flat_id,
        building_id=building_id,
        building__owner__phone=phone
    )

    # Deactivate active tenant
    Tenant.objects.filter(flat=flat, is_active=True).update(is_active=False)

    return redirect('flatDetails', building_id=building_id, flat_id=flat_id)


# -------------------- TENANT DETAILS --------------------

def tenantDetails(request, building_id, flat_id, tenant_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    tenant = get_object_or_404(
        Tenant, id=tenant_id, flat_id=flat_id,
        flat__building_id=building_id,
        flat__building__owner__phone=phone
    )

    return render(request, 'tenant/tenantDetails.html', {
        'tenant': tenant,
        'flat': tenant.flat,
        'building': tenant.flat.building,
    })


# -------------------- PAST TENANTS --------------------

def pastTenants(request, building_id, flat_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    flat = get_object_or_404(
        Flat, id=flat_id,
        building_id=building_id,
        building__owner__phone=phone
    )

    past = Tenant.objects.filter(is_active=False, flat_id=flat_id).order_by('-date_added')

    return render(request, 'tenant/pastTenants.html', {
        'flat': flat,
        'tenants': past
    })



def tenantPaymentHistory(request, building_id, flat_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    # Validate flat belongs to this owner
    flat = get_object_or_404(
        Flat,
        id=flat_id,
        building_id=building_id,
        building__owner__phone=phone
    )

    # Latest active tenant
    tenant = flat.tenants.order_by('-date_added').first()

    if not tenant:
        payments = []
    else:
        payments = RentPayment.objects.filter(
            tenant=tenant,
            flat=flat
        ).order_by('-id')  # newest record always at top


    return render(request, 'tenant/tenantPaymentHistory.html', {
        'flat': flat,
        'tenant': tenant,
        'payments': payments,
    })



def tenantFullDetails(request, tenant_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    # Fetch tenant, but ensure the owner truly owns the building this tenant stayed in
    tenant = get_object_or_404(
        Tenant,
        id=tenant_id,
        flat__building__owner__phone=phone
    )

    payments = RentPayment.objects.filter(
        tenant=tenant
    ).order_by('-id')

    flat = tenant.flat
    building = flat.building
    owner = building.owner

    return render(request, 'tenant/tenantFullDetails.html', {
        'tenant': tenant,
        'payments': payments,
        'flat': flat,
        'building': building,
        'owner': owner
    })


def tenantAllTransactions(request, tenant_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    # Ensure owner can only see their own tenant
    tenant = get_object_or_404(
        Tenant,
        id=tenant_id,
        flat__building__owner__phone=phone
    )

    payments = RentPayment.objects.filter(
        tenant=tenant
    ).order_by('-id')

    flat = tenant.flat
    building = flat.building
    owner = building.owner

    return render(request, 'tenant/tenantAllTransactions.html', {
        'tenant': tenant,
        'payments': payments,
        'flat': flat,
        'building': building,
        'owner': owner
    })
