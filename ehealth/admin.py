from django.contrib import admin
from .models import Patient, MedRecord

# Register your models here.
admin.site.register(Patient)
admin.site.register(MedRecord)
