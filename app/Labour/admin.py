from django.contrib import admin
from .models import LabourService, PayPeriod
# Register your models here.

admin.site.register(LabourService)
# admin.site.register(LaboursRequest)
admin.site.register(PayPeriod)
