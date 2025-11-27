from django.urls import path
from . import views

urlpatterns = [
    path('', views.tenantHome, name='tenantHome'),
    path('loginTenant/', views.loginTenant, name='loginTenant'),
    path('add/<int:flat_id>/', views.addTenant, name='addTenant'),

]
