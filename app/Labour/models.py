from django.db import models
from Wards.models import Ward
from Farm.models import Farm
from Buyer.models import Buyer


# Create your models here.

class LabourService(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()

    def __str__(self):
        return self.title


class LaboursRequest(models.Model):
    PERIOD_CHOICES = [('1', "Day"), ('2', "Week"), ('3', "Month")]
    ward = models.ForeignKey(Ward, related_name="labourServiceRequest", on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True, related_name="LabourRequests", blank=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, related_name="LabourRequests", blank=True)
    service = models.ForeignKey(LabourService, on_delete=models.CASCADE, null=False)
    startDate = models.DateTimeField(null=False)
    periodNumber = models.IntegerField(null=False)
    pay = models.FloatField(null=False)
    payPeriod = models.CharField(max_length=30, choices=PERIOD_CHOICES, default=1)

    def __str__(self):
        return self.id
