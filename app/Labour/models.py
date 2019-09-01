from django.db import models


# Create your models here.

class LabourServices(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()

    def __str__(self):
        return self.title
