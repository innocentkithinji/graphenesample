from Buyer.models import Buyer
from Farm.models import Farm
from Wards.models import Ward
from django.db import models


# Create your models here.

class LabourService(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()

    def __str__(self):
        return self.title


class PayPeriod(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaboursRequest(models.Model):
    PERIOD_CHOICES = [('1', "Day"), ('2', "Week"), ('3', "Month")]
    ward = models.ForeignKey(Ward, related_name="labourServiceRequest", on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True, related_name="LabourRequests", blank=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, related_name="LabourRequests", blank=True)
    service = models.ForeignKey(LabourService, on_delete=models.CASCADE, null=False)
    startDate = models.DateTimeField(null=False)
    periodNumber = models.IntegerField(null=False)
    pay = models.FloatField(null=False)
    workers = models.IntegerField()
    payPeriod = models.ForeignKey(PayPeriod, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class LabourApplication(models.Model):
    from Labourers.models import Labourer

    LaboursRequest = models.ForeignKey(LaboursRequest, related_name="labourApplication", on_delete=models.CASCADE)
    Labourer = models.ForeignKey(Labourer, related_name="LabourerApplications", on_delete=models.CASCADE)
    hired = models.BooleanField(default=False, null=False)
    responded = models.BooleanField(default=False, null=False)
