from django.db import models
from County.models import County
from Packages.models import FarmPackage
from Members.models import Member
from Wards.models import Ward

# Create your models here.
class Farm(models.Model):
    name = models.CharField(max_length=50)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="farms")
    Ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="farms", null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    package = models.ForeignKey(FarmPackage, on_delete=models.SET_NULL, null=True)
    package_update_date = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(True)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="farms", blank=True)

    def __str__(self):
        return self.name
