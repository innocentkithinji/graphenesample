from django.db import models

# Create your models here.
class Unit(models.Model):
    name = models.CharField(max_length=60)
    alternative_name = models.CharField(max_length=60, null=True)

    def __str__(self):
        return self.name