from django.db import models
from Packages.models import LabourersPackage
from Wards.models import Ward
from Members.models import Member
from Labour.models import LabourService
import random


# Create your models here.
class Labourer(models.Model):
    name = models.CharField(max_length=30)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    package = models.ForeignKey(LabourersPackage, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='labourProfile', )
    services = models.ManyToManyField(LabourService, related_name="LabourProvider")
    packages_buying_Date = models.DateTimeField(auto_now_add=True)
    account = models.CharField(max_length=30, unique=True, default=f"LR{random.randint(1, 999999)}")

    def __str__(self):
        return self.name
