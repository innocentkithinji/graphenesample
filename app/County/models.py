from django.db import models
from Country.models import Country
# Create your models here.

class County(models.Model):
    name = models.CharField(max_length=50);
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="counties")

    def __str__(self):
        return self.name