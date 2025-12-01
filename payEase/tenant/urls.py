from django.urls import path
from . import views

urlpatterns = [
    path('', views.tenantHome, name='tenantHome'),

    path('loginTenant/', views.loginTenant, name='loginTenant'),

    path('dashboard/', views.tenantDashboard, name='tenantDashboard'),

    path('allFlats/', views.allFlats, name='allFlats'),

    path('logout/', views.logoutTenant, name='logoutTenant'),

    path('payRent/', views.payRent, name='payRent'),

]

