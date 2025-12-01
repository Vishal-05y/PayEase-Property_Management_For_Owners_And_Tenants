from django.urls import path
from . import views

urlpatterns = [
    path('', views.tenantHome, name='tenantHome'),

    path('loginTenant/', views.loginTenant, name='loginTenant'),

    path('dashboard/', views.tenantDashboard, name='tenantDashboard'),

    path('allFlats/', views.allFlats, name='allFlats'),

    path('flat/<int:flat_id>/', views.flatDetails, name='flatDetails'),


    path('logout/', views.logoutTenant, name='logoutTenant'),


    # Pay Rent
    path('payRent/', views.payRent, name='payRent'),

    path('rentHistory/', views.rentHistory, name='rentHistory'),

    path('flat/<int:flat_id>/transactions/', views.tenantFlatTransactions, name='tenantFlatTransactions'),

    path('processPayment/', views.processPayment, name='processPayment'),
    
    path('paymentSuccess/', views.paymentSuccess, name='paymentSuccess'),

    path('checkDue/', views.tenantCheckDue, name='tenantCheckDue'),

]

