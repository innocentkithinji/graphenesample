from django.contrib import admin

# Register your models here.
from .models import BuyerPackage, FarmPackage, Period, LabourersPackage

admin.site.register(BuyerPackage)
admin.site.register(FarmPackage)
admin.site.register(LabourersPackage)
admin.site.register(Period)
