from django.urls import path
from . import views

urlpatterns = [
    path('', views.ownerHome, name='ownerHome'),
    path('loginOwner/', views.loginOwner , name='loginOwner'),

    # Viewing the page with object id as url
    path('<int:tenant_id>/', views.tenantDetails, name='tenant_details'),

    # Viewing the page with object id as url
    path('buildingsList/<int:building_id>/', views.buildingDetails, name='buildingDetails'),

    path('flatsList/', views.flatsList, name='flatsList'),

    path('buildingsList/', views.buildingsList, name='buildingsList'),

    path('building/add/', views.addBuilding, name='addBuilding'),

    path('buildings/<int:building_id>/addFlat/', views.addFlat, name='addFlat'),

    path('buildingsList/<int:building_id>/flat/<int:flat_id>/', views.flatDetails, name='flatDetails'),


]