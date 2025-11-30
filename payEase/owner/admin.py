from django.contrib import admin
from .models import Flat, Building, Owner

# Register your models here.
admin.site.register(Owner)

admin.site.register(Flat)

admin.site.register(Building)
