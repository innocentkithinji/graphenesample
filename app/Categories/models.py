from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    alternative_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True, upload_to="media/")

    def __str__(self):
        return self.name

