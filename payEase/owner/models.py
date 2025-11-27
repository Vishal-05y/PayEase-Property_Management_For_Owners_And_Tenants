from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    cost = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Flat(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='flats')
    flat_number = models.CharField(max_length=20)   # Example: "101", "G1", "PH1"
    flat_type = models.CharField(max_length=50)     # Example: "2BHK", "Single Room"

    def __str__(self):
        return f"{self.flat_number} ({self.flat_type}) - {self.building.name}"
