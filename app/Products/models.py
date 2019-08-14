from django.db import models
from Categories.models import Category
from Units.models import Unit


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    alternative_name = models.CharField(max_length=50)
    units_of_measure = models.ManyToManyField(Unit, related_name='products')
    product_category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name="products")
    image = models.ImageField(blank=True, null=True, upload_to="media/")

    def __str__(self):
        return self.name
