from django.db import models
from County.models import County


# Create your models here.

class Ward(models.Model):
    name = models.CharField(max_length=50)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="wards")

    def __str__(self):
        return self.name