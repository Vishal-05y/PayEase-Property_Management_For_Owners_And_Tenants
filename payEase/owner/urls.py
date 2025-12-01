from django.urls import path
from . import views

urlpatterns = [
    path('', views.ownerHome, name='ownerHome'),

    path('signUpOwner/', views.signUpOwner , name='signUpOwner'),

    path('loginOwner/', views.loginOwner , name='loginOwner'),

    path('dashboard/', views.ownerDashboard, name='ownerDashboard'),

    path('building/add/', views.addBuilding, name='addBuilding'),

    path('buildings/<int:building_id>/', views.buildingDetails, name='buildingDetails'),

    path('buildings/<int:building_id>/addFlat/', views.addFlat, name='addFlat'),

    path('buildings/<int:building_id>/flat/<int:flat_id>/', views.flatDetails, name='flatDetails'),

    path('buildings/<int:building_id>/flat/<int:flat_id>/addTenant/', views.addTenant, name='addTenant'),

    path('buildings/<int:building_id>/flat/<int:flat_id>/remove/', views.removeTenant, name='removeTenant'),

    path('buildings/<int:building_id>/flat/<int:flat_id>/pastTenants/', views.pastTenants, name='pastTenants'),

    path('tenant/<int:tenant_id>/details/', views.tenantFullDetails, name='tenantFullDetails'),

    path('tenant/<int:tenant_id>/transactions/', views.tenantAllTransactions, name='tenantAllTransactions'),

    path('buildings/<int:building_id>/flat/<int:flat_id>/tenant/<int:tenant_id>/', views.tenantDetails, name='tenantDetails'),

    path('logout/', views.logoutOwner, name='logoutOwner'),


    path('buildings/<int:building_id>/flat/<int:flat_id>/tenant/payment-history/', views.tenantPaymentHistory, name='tenantPaymentHistory'),


]

