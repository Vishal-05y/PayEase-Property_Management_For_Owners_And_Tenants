from django.urls import path
from . import views

urlpatterns = [
    path('', views.tenantHome, name='tenantHome'),
    path('loginTenant/', views.loginTenant, name='loginTenant')
]
