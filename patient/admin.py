from django.contrib import admin
from .models import *

admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Message)
admin.site.register(Feedback)
admin.site.register(UserProfile)
admin.site.register(PatientSurvey)
admin.site.register(MedicalConsent)


