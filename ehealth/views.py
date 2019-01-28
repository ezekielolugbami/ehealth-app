from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import PatientForm, MedRecordForm, UserForm
from .models import Patient, MedRecord
# Create your views here.

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_patient(request):
    if not request.user.is_authenticated():
        return render(request, 'ehealth/login.html')
    else:
        form = PatientForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.pat_img = request.FILES['pat_img']
            file_type = patient.pat_img.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'patient': patient,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'ehealth/create_patient.html', context)
            patient.save()
            return render(request, 'ehealth/detail.html', {'patient': patient})
        context = {
            "form": form,
        }
        return render(request, 'ehealth/create_patient.html', context)


def create_medrecord(request, patient_id):
    form = MedRecordForm(request.POST or None, request.FILES or None)
    patient = get_object_or_404(Patient, pk=patient_id)
    if form.is_valid():
        patients_medrecords = patient.medrecord_set.all()
        for s in patients_medrecords:
            if s.chief_complaint == form.cleaned_data.get("chief_complaint"):
                context = {
                    'patient': patient,
                    'form': form,
                    'error_message': 'You already added that medrecord',
                }
                return render(request, 'ehealth/create_medrecord.html', context)
        medrecord = form.save(commit=False)
        medrecord.patient = patient
        

        medrecord.save()
        return render(request, 'ehealth/detail.html', {'patient': patient})
    context = {
        'patient': patient,
        'form': form,
    }
    return render(request, 'ehealth/create_medrecord.html', context)



def delete_patient(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    patient.delete()
    patients = Patient.objects.filter(user=request.user)
    return render(request, 'ehealth/index.html', {'patients': patients})


def delete_medrecord(request, patient_id, medrecord_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    medrecord = MedRecord.objects.get(pk=medrecord_id)
    medrecord.delete()
    return render(request, 'ehealth/detail.html', {'patient': patient})





def index(request):
    if not request.user.is_authenticated():
        return render(request, 'ehealth/login.html')
    else:
        patients = Patient.objects.filter(user=request.user)
        medrecord_results = MedRecord.objects.all()
        query = request.GET.get("q")
        if query:
            patients = patients.filter(
                Q(pat_name__icontains=query) |
                Q(clinician__icontains=query)
            ).distinct()
            medrecord_results = medrecord_results.filter(
                Q(chief_complaint__icontains=query)
            ).distinct()
            return render(request, 'ehealth/index.html', {
                'patients': patients,
                'medrecords': medrecord_results,
            })
        else:
            return render(request, 'ehealth/index.html', {'patients': patients})




def detail(request, patient_id):
    if not request.user.is_authenticated():
        return render(request, 'ehealth/login.html')
    else:
        user = request.user
        patient = get_object_or_404(Patient, pk=patient_id)
        return render(request, 'ehealth/detail.html', {'patient': patient, 'user': user})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'ehealth/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                patients = Patient.objects.filter(user=request.user)
                return render(request, 'ehealth/index.html', {'patients': patients})
            else:
                return render(request, 'ehealth/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'ehealth/login.html', {'error_message': 'Invalid login'})
    return render(request, 'ehealth/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                patients = Patient.objects.filter(user=request.user)
                return render(request, 'ehealth/index.html', {'patients': patients})
    context = {
        "form": form,
    }
    return render(request, 'ehealth/register.html', context)


def medrecords(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'ehealth/login.html')
    else:
        try:
            medrecord_ids = []
            for patient in Patient.objects.filter(user=request.user):
                for medrecord in patient.medrecord_set.all():
                    medrecord_ids.append(medrecord.pk)
            users_medrecords = MedRecord.objects.filter(pk__in=medrecord_ids)
            # if filter_by == 'chief_complaint':
            #     users_medrecords = users_medrecords.filter(is_favorite=True)
        except Patient.DoesNotExist:
            users_medrecords = []
        return render(request, 'ehealth/medrecords.html', {
            'medrecord_list': users_medrecords,
            'filter_by': filter_by,
        })
