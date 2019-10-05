from django.db import models
from County.models import County
from Packages.models import FarmPackage
from Members.models import Member
from Wards.models import Ward
import random


# Create your models here.

def uniqueacoount():
    account = f"FM{random.randint(1, 9)}{random.randint(111, 999)}{random.randint(111, 888)}"
    Query = Farm.objects.get(accounts=account)
    if Query.len() == 0:
        uniqueacoount()
    return account


class Farm(models.Model):
    name = models.CharField(max_length=50)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="farms")
    Ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="farms", null=True)
    package = models.ForeignKey(FarmPackage, on_delete=models.SET_NULL, null=True)
    package_update_date = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(True)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="farms", blank=True)
    accounts = models.CharField(max_length=20, blank=False, null=False, unique=True,
                                default=uniqueacoount())

    def __str__(self):
        return self.name
