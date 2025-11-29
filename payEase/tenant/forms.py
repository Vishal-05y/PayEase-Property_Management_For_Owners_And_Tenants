from django import forms
from .models import Tenant

class addTenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'phone', 'flat_price']


class loginTenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'phone']