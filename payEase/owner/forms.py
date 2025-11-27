from django import forms
from .models import Building, Flat

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'address', 'cost']


class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = ['flat_number', 'flat_type']
