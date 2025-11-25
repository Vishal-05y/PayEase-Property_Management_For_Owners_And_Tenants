from django.urls import path
from . import views

urlpatterns = [
    path('', views.ownerHome, name='ownerHome'),
    path('loginOwner/', views.loginOwner , name='loginOwner'),
]