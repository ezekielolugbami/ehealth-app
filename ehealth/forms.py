from django import forms
from django.contrib.auth.models import User

from .models import Patient, MedRecord


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['clinician', 'pat_name', 'bloodtype', 'pat_img', 'contact']


class MedRecordForm(forms.ModelForm):

    class Meta:
        model = MedRecord
        fields = ['chief_complaint', 'gender', 'medications']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
