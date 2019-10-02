from django.db import models


# Create your models here.
class payRequest(models.Model):
    phone = models.CharField(max_length=30)
    account = models.CharField(max_length=30)
    amount = models.CharField(max_length=40)
    posted = models.BooleanField()