from django.db import models
from County.models import County
from Products.models import Product


# Create your models here.
class Prices(models.Model):
    price = models.IntegerField(null=False)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
