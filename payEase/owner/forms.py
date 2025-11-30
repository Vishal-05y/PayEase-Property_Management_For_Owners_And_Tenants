from django import forms
from .models import Building, Flat, Owner

class SignUpOwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'phone']


class LoginOwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'phone']

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'address', 'cost']


class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = ['flat_number', 'flat_type']
