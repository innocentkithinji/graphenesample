from django.db import models


# Create your models here.
class Period(models.Model):
    name = models.CharField(max_length=40)
    number_of_days = models.IntegerField()

    def __str__(self):
        return self.name


class FarmPackage(models.Model):
    name = models.CharField(max_length=30)
    number_of_bids = models.IntegerField()
    number_of_products = models.IntegerField()
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True, related_name="FPackage")
    price = models.IntegerField()

    def __str__(self):
        return self.name


class BuyerPackage(models.Model):
    name = models.CharField(max_length=30)
    searches = models.BooleanField()
    total_bid_placed = models.IntegerField()
    broadCastAbility = models.BooleanField()
    price = models.IntegerField()
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True, related_name="BPackage")

    def __str__(self):
        return self.name
