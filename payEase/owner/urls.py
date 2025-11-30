from django.urls import path
from . import views

urlpatterns = [
    path('', views.ownerHome, name='ownerHome'),

    path('signUpOwner/', views.signUpOwner , name='signUpOwner'),

    path('loginOwner/', views.loginOwner , name='loginOwner'),

    path('<int:phone>/dashboard/', views.ownerDashboard, name='ownerDashboard'),

    path('<int:phone>/building/add/', views.addBuilding, name='addBuilding'),

    path('<int:phone>/buildingsList/<int:building_id>/', views.buildingDetails, name='buildingDetails'),

    path('<int:phone>/buildings/<int:building_id>/addFlat/', views.addFlat, name='addFlat'),

    path('<int:phone>/buildingsList/<int:building_id>/flat/<int:flat_id>/', views.flatDetails, name='flatDetails'),

    path('buildingsList/<int:building_id>/flat/<int:flat_id>/tenant/<int:tenant_id>/', views.tenantDetails, name='tenantDetails'),
    
    path('<int:phone>/buildingsList/<int:building_id>/flat/<int:flat_id>/pastTenants/', views.pastTenants, name='pastTenants'),
]
