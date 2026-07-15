from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    PIPELINE_STATUS = [
        ('FOUND', 'Found'),
        ('SCHEDULED', 'Viewing Scheduled'),
        ('APPLIED', 'Applied'),
        ('SIGNED', 'Lease Signed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=PIPELINE_STATUS, default='FOUND')
    
    campus_distance = models.FloatField(help_text="Distance in miles")
    transit_proximity = models.IntegerField(help_text="Scale 1-5")
    wifi_capability = models.IntegerField(help_text="Scale 1-5")

    def __str__(self):
        return self.address