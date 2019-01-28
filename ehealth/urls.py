from django.conf.urls import url
from . import views

app_name = 'ehealth'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<patient_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^medrecords/(?P<filter_by>[a-zA_Z]+)/$', views.medrecords, name='medrecords'),
    url(r'^create_patient/$', views.create_patient, name='create_patient'),
    url(r'^(?P<patient_id>[0-9]+)/create_medrecord/$', views.create_medrecord, name='create_medrecord'),
    url(r'^(?P<patient_id>[0-9]+)/delete_medrecord/(?P<medrecord_id>[0-9]+)/$', views.delete_medrecord, name='delete_medrecord'),
    url(r'^(?P<patient_id>[0-9]+)/delete_patient/$', views.delete_patient, name='delete_patient'),

]
