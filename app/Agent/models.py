import random

from django.db import models


# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    code = models.IntegerField(unique=True, default=random.randint(1, 999999))

    def __str__(self):
        return self.code