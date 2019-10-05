from django.db import models
from County.models import County
from Packages.models import BuyerPackage
from Members.models import Member


# Create your models here.
class Buyer(models.Model):
    name = models.CharField(max_length=30)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    package = models.ForeignKey(BuyerPackage, on_delete=models.SET_NULL, blank=True)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='buyingProfile', )
    packages_buying_Date = models.DateTimeField(auto_now_add=True)
    account = models.CharField(max_length=20, blank=True, unique=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
