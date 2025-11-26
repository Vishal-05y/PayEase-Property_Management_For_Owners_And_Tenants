from django.db import models
from django.utils import timezone

class Tenant(models.Model):
    FLATS_CHOICES = [
        ('G1', 'GROUND FLOOR-1BHK'),
        ('G2', 'GROUND FLOOR-SINGLE ROOM'),
        ('F1', 'FIRST FLOOR-3BHK'),
        ('F21', 'SECOND FLOOR-2BHK'),
        ('F22', 'SECOND FLOOR-1BHK'),
        ('F31', 'PENT HOUSE-FRONT'),
        ('F32', 'PENT HOUSE-BACK'),
    ]

    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)  # tenant phone number
    flat_price = models.PositiveIntegerField()  # monthly rent price
    date_added = models.DateTimeField(default=timezone.now)

    type = models.CharField(max_length=5, choices=FLATS_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
