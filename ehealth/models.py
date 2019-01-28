from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.

class Patient(models.Model):
    user = models.ForeignKey(User, default=1)
    clinician = models.CharField(max_length=250)
    pat_name = models.CharField(max_length=500)
    bloodtype = models.CharField(max_length=100)
    pat_img = models.FileField()
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.pat_name + ' - ' + self.clinician


class MedRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    chief_complaint = models.CharField(max_length=250)
    gender = models.CharField(max_length=250)
    medications = models.CharField(max_length=500)

    def __str__(self):
        return self.chief_complaint
