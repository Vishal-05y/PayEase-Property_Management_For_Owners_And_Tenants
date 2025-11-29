from django.urls import path
from . import views

urlpatterns = [
    path('', views.tenantHome, name='tenantHome'),
    path('loginTenant/', views.loginTenant, name='loginTenant'),
    path('dashboard/<int:phone>/', views.tenantDashboard, name='tenantDashboard'),
    path('dashboard/<int:phone>/allFlats', views.allFlats, name='allFlats'),
    # path('add/<int:flat_id>/', views.addTenant, name='addTenant'),

    # path('buildingsList/<int:building_id>/flat/<int:flat_id>/', views.tenantDetails, name='viewDetails'),

    path('buildingsList/<int:building_id>/flat/<int:flat_id>/addTenant/', views.addTenant, name='addTenant'),
]
