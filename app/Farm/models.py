from django.db import models
from County.models import County
from Packages.models import FarmPackage
from Members.models import Member
from Wards.models import Ward
import random


# Create your models here.

def uniqueacoount():
    while True:
        account = f"FM{random.randint(1, 9)}{random.randint(111, 999)}{random.randint(111, 888)}"
        query = Farm.objects.filter(accounts=account).exists()
        if not query:
            return account


class Farm(models.Model):
    name = models.CharField(max_length=50)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="farms")
    Ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="farms", null=True)
    package = models.ForeignKey(FarmPackage, on_delete=models.SET_NULL, null=True)
    package_update_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="farms", blank=True)
    accounts = models.CharField(max_length=20, blank=True, null=True, unique=True)
    active = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.name
