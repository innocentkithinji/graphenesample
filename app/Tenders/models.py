from django.db import models
from County.models import County
from Buyer.models import Buyer
from Products.models import Product
from Units.models import Unit
from Farm.models import Farm


# Create your models here.
class Tender(models.Model):
    buyer = models.ForeignKey(Buyer, null=False, on_delete=models.CASCADE, related_name="tenders")
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, related_name="tenders")
    county = models.ForeignKey(County, null=False, on_delete=models.CASCADE, related_name="tenders")
    amount = models.FloatField()
    unit = models.ForeignKey(Unit, null=True, on_delete=models.SET_NULL)


class Bid(models.Model):
    farm = models.ForeignKey(Farm, null=False, on_delete=models.CASCADE, related_name="bids")
    county = models.ForeignKey(County, null=False, on_delete=models.CASCADE, related_name="bids")
    price = models.IntegerField(null=False)
    Amount = models.IntegerField(null=False)
    Unit = models.ForeignKey(Unit , null=True, on_delete=models.SET_NULL)
