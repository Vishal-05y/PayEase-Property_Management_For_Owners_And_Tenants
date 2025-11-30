from tenant.models import Tenant
from django.shortcuts import render, redirect, get_object_or_404
from .models import Building, Flat, Owner
from .forms import BuildingForm, FlatForm, LoginOwnerForm, SignUpOwnerForm
from django.http import Http404, HttpResponse

# Create your views here.
def ownerHome(request):
    return render(request, 'owner/ownerHome.html')


def signUpOwner(request):
    if request.method == 'POST':
        form = SignUpOwnerForm(request.POST)
        
        if form.is_valid():
            phone = form.cleaned_data['phone']

            # Check if phone already registered
            if Owner.objects.filter(phone=phone).exists():
                return render(request, 'owner/signUpOwner.html', {
                    'form': form,
                    'error': "Number is already registered."
                })

            # If not exists → save
            form.save()
            return redirect('loginOwner')

    else:
        form = SignUpOwnerForm()

    # DEFAULT RENDER
    return render(request, 'owner/signUpOwner.html', {'form': form})


def loginOwner(request):
    if request.method == 'POST':
        form = LoginOwnerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']

            owner = Owner.objects.filter(name=name, phone=phone)

            if owner.exists():
                return redirect('ownerDashboard', phone=phone)
            else:
                return render(request, 'owner/loginOwner.html', {
                    'form': form,
                    'error': "No owner found with this phone number."
                })
    else:
        form = LoginOwnerForm()

    return render(request, 'owner/loginOwner.html', {'form': form})


def ownerDashboard(request, phone):

    # Get the owner using phone
    owner = Owner.objects.filter(phone=phone).first()

    if not owner:
        return HttpResponse("Owner not found")

    # Get buildings belonging to this owner ONLY
    buildings = Building.objects.filter(owner=owner)

    # Flats inside owner buildings
    flats = Flat.objects.filter(building__owner=owner)

    # Occupied flats (which have tenants)
    occupied_flats = Tenant.objects.filter(flat__building__owner=owner).values('flat').distinct().count()

    total_buildings = buildings.count()
    total_flats = flats.count()
    vacant_flats = total_flats - occupied_flats

    return render(request, "owner/ownerDashboard.html", {
        "owner": owner,
        "phone": phone,
        "buildings": buildings,

        # Stats only for this owner
        "total_buildings": total_buildings,
        "total_flats": total_flats,
        "occupied_flats": occupied_flats,
        "vacant_flats": vacant_flats,
    })

    
def addBuilding(request, phone):
    owner = get_object_or_404(Owner, phone=phone)

    if request.method == "POST":
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save(commit=False)
            building.owner = owner
            building.save()
            return redirect('ownerDashboard', phone)
    else:
        form = BuildingForm()

    return render(request, 'building/addBuilding.html', {
        'form': form,
        'owner': owner
    })


def buildingDetails(request, phone, building_id):
    building = get_object_or_404(Building, pk=building_id)
    flats = building.flats.all()
    return render(request, 'building/buildingDetails.html', {
        'building': building,
        'flats': flats,
        'phone':phone,
    })


def addFlat(request, phone, building_id):
    building = get_object_or_404(Building, pk=building_id)

    if request.method == "POST":
        form = FlatForm(request.POST)
        if form.is_valid():
            flat = form.save(commit=False)
            flat.building = building
            flat.save()
            return redirect('ownerDashboard', phone)
    else:
        form = FlatForm()

    return render(request, 'flat/addFlat.html', {
        'phone': phone,
        'form': form, 
        'building': building
    })


def flatDetails(request, phone, building_id, flat_id):
    flat = get_object_or_404(Flat, id=flat_id, building_id=building_id)

    # Get the most recent tenant for this flat
    latest_tenant = flat.tenants.order_by('-date_added').first()

    return render(request, 'flat/flatDetails.html', {
        'phone': phone,
        'flat': flat,
        'tenant': latest_tenant,
        'building_id': building_id,   # IMPORTANT: add this
    })


def tenantDetails(request, building_id, flat_id, tenant_id):

    # Get tenant using only valid fields
    tenant = get_object_or_404(Tenant, id=tenant_id, flat_id=flat_id)

    # Ensure tenant belongs to the correct building
    if tenant.flat.building_id != building_id:
        raise Http404("Tenant not in this building")

    return render(request, 'tenant/tenantDetails.html', {
        'tenant': tenant,
        'flat': tenant.flat,
        'building': tenant.flat.building,
    })


def pastTenants(request, phone, building_id, flat_id):
    flat = get_object_or_404(Flat, id=flat_id, building_id=building_id)

    # Get the most recent tenant for this flat
    past_tenants = Tenant.objects.filter(flat_id = flat_id).order_by('-date_added')

    return render(request, 'tenant/pastTenants.html', {
        'phone': phone,
        'flat': flat,
        'tenants': past_tenants,
        'building_id': building_id,   # IMPORTANT: add this
    })
