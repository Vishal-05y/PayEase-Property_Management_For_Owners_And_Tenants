from django.db import models
from django.utils import timezone
from owner.models import Flat   # IMPORTANT

class Tenant(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='tenants')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    flat_price = models.PositiveIntegerField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} in {self.flat.flat_number}"
