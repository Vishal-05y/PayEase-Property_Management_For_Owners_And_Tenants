from django.urls import path
from . import views

urlpatterns = [
    path('', views.tenantHome, name='tenantHome'),

    # Authentication
    path('loginTenant/', views.loginTenant, name='loginTenant'),

    path('logout/', views.logoutTenant, name='logoutTenant'),

    # Dashboard
    path('dashboard/', views.tenantDashboard, name='tenantDashboard'),


    # Building
    path("gallery/building/", views.tenantBuildingGallery, name="tenantBuildingGallery"),


    # Flat
    path('flat/<int:flat_id>/', views.flatDetails, name='flatDetails'),

    path('allFlats/', views.allFlats, name='allFlats'),

    path("gallery/flat/", views.tenantFlatGallery, name="tenantFlatGallery"),


    # Payment
    path('payRent/', views.payRent, name='payRent'),

    path('processPayment/', views.processPayment, name='processPayment'),

    path('paymentSuccess/', views.paymentSuccess, name='paymentSuccess'),

    path('rentHistory/', views.rentHistory, name='rentHistory'),

    path('flat/<int:flat_id>/transactions/', views.tenantFlatTransactions, name='tenantFlatTransactions'),

    path('checkDue/', views.tenantCheckDue, name='tenantCheckDue'),

]

