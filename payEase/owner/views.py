from tenant.models import Tenant
from django.db.models import Max
from .forms import BuildingForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Building, Flat
from .forms import BuildingForm, FlatForm

# Create your views here.

# To get model into view page only recently added tenants
def ownerHome(request):
    buildings = Building.objects.all()

    # Dashboard stats
    total_buildings = buildings.count()
    total_flats = Flat.objects.count()
    occupied_flats = Tenant.objects.values('flat').distinct().count()
    vacant_flats = total_flats - occupied_flats

    return render(request, "owner/ownerHome.html", {
        "buildings": buildings,
        "total_buildings": total_buildings,
        "total_flats": total_flats,
        "occupied_flats": occupied_flats,
        "vacant_flats": vacant_flats,
    })

    

def loginOwner(request):
    return render(request, 'owner/loginOwner.html')


# To get object details using url
def tenantDetails(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    return render(request, 'owner/tenant_details.html', {'tenant':tenant})


def buildingDetails(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    flats = building.flats.all()
    return render(request, 'owner/buildingDetails.html', {
        'building': building,
        'flats': flats,
    })



def flatsList(request):
    flat_type = request.GET.get('type')   # read selected type

    FLAT_TYPES = [
        ('G1', 'GROUND FLOOR-1BHK'),
        ('G2', 'GROUND FLOOR-SINGLE ROOM'),
        ('F21', 'SECOND FLOOR-2BHK'),
        ('F22', 'SECOND FLOOR-1BHK'),
        ('F31', 'PENT HOUSE-FRONT'),
        ('F32', 'PENT HOUSE-BACK'),
    ]

    # If a type is selected, filter
    if flat_type:
        flats_list = Tenant.objects.filter(type=flat_type)
    else:
        flats_list = None   # nothing selected yet

    context = {
        'flats_list': flats_list,
        'flat_type': flat_type,
        'flat_choices': FLAT_TYPES,
    }
    return render(request, 'owner/flatsList.html', context)


def addBuilding(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ownerHome')  # redirect to owner home after saving
    else:
        form = BuildingForm()

    return render(request, 'owner/addBuilding.html', {'form': form})


def buildingsList(request):
    buildings = Building.objects.all()
    return render(request, 'owner/buildingsList.html', {'buildings': buildings})


def addFlat(request, building_id):
    building = get_object_or_404(Building, pk=building_id)

    if request.method == "POST":
        form = FlatForm(request.POST)
        if form.is_valid():
            flat = form.save(commit=False)
            flat.building = building
            flat.save()
            return redirect('buildingDetails', building_id=building.id)
    else:
        form = FlatForm()

    return render(request, 'owner/addFlat.html', {'form': form, 'building': building})


def flatDetails(request, building_id, flat_id):
    flat = get_object_or_404(Flat, id=flat_id, building_id=building_id)

    # Get the most recent tenant for this flat
    latest_tenant = flat.tenants.order_by('-date_added').first()

    return render(request, 'owner/flatDetails.html', {
        'flat': flat,
        'tenant': latest_tenant,
        'building_id': building_id,   # IMPORTANT: add this
    })
