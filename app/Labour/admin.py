from django.contrib import admin
from .models import LabourService, LaboursRequest, PayPeriod
# Register your models here.

admin.site.register(LabourService)
admin.site.register(LaboursRequest)
admin.site.register(PayPeriod)
