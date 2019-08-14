from django.db import models
from Farm.models import Farm
from Units.models import Unit
from Products.models import Product
from County.models import County


# Create your models here.
class Sale(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    amount = models.FloatField(null=False)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, related_name="selling")
    price = models.FloatField()
