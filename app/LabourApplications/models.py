from django.db import models
from Labourers.models import Labourer
from Labour.models import LaboursRequest
# Create your models here.
class LabourApplication(models.Model):

    LaboursRequest = models.ForeignKey(LaboursRequest, related_name="labourApplication", on_delete=models.CASCADE)
    Labourer = models.ForeignKey(Labourer, related_name="LabourerApplications", on_delete=models.CASCADE)
    hired = models.BooleanField(default=False, null=False)
    responded = models.BooleanField(default=False, null=False)