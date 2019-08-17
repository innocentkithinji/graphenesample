from django.contrib import admin

# Register your models here.
from .models import BuyerPackage, FarmPackage

admin.site.register(BuyerPackage)
admin.site.register(FarmPackage)
