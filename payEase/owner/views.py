from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import Owner, Building, Flat
from tenant.models import Tenant
from .forms import SignUpOwnerForm, LoginOwnerForm, BuildingForm, FlatForm, addTenantForm

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

    occupied = Tenant.objects.filter(flat__building__owner=owner).values('flat').distinct().count()

    return render(request, "owner/ownerDashboard.html", {
        "owner": owner,
        "buildings": buildings,
        "total_buildings": buildings.count(),
        "total_flats": flats.count(),
        "occupied_flats": occupied,
        "vacant_flats": flats.count() - occupied,
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

    building = get_object_or_404(Building, id=building_id, owner__phone=phone)
    return render(request, 'building/buildingDetails.html', {
        'building': building,
        'flats': building.flats.all(),
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
        Flat, id=flat_id,
        building_id=building_id,
        building__owner__phone=phone
    )

    latest_tenant = flat.tenants.order_by('-date_added').first()

    return render(request, 'flat/flatDetails.html', {
        'flat': flat,
        'tenant': latest_tenant,
    })


# -------------------- ADD TENANT (OWNER SIDE) --------------------

def addTenant(request, building_id, flat_id):
    phone = request.session.get('owner_phone')
    if not phone:
        return redirect('loginOwner')

    flat = get_object_or_404(
        Flat, id=flat_id,
        building_id=building_id,
        building__owner__phone=phone
    )

    if request.method == "POST":
        form = addTenantForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            tphone = form.cleaned_data['phone']
            flat_price = form.cleaned_data['flat_price']

            try:
                existing = Tenant.objects.get(flat=flat, phone=tphone)
                existing.name = name
                existing.flat_price = flat_price
                existing.date_added = timezone.now()
                existing.save()

            except Tenant.DoesNotExist:
                tenant = form.save(commit=False)
                tenant.flat = flat
                tenant.save()

            return redirect('flatDetails', building_id=building_id, flat_id=flat_id)

    else:
        form = addTenantForm()

    return render(request, 'tenant/addTenant.html', {
        'form': form,
        'flat': flat
    })


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

    past = Tenant.objects.filter(flat_id=flat_id).order_by('-date_added')

    return render(request, 'tenant/pastTenants.html', {
        'flat': flat,
        'tenants': past
    })
