from django.urls import path
from . import views

urlpatterns = [
    path('', views.tenantHome, name='tenantHome'),

    path('loginTenant/', views.loginTenant, name='loginTenant'),

    path('<int:phone>/dashboard', views.tenantDashboard, name='tenantDashboard'),
    
    path('<int:phone>/allFlats', views.allFlats, name='allFlats'),

    path('<int:phone>/buildingsList/<int:building_id>/flat/<int:flat_id>/addTenant/', views.addTenant, name='addTenant'),
]
