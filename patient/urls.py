from django.urls import path
from .views import *

app_name = "patient"

from .views import (
    book_appointment, view_appointments, view_history, send_message, inbox,
    AppointmentUpdateView, AppointmentDeleteView,
    MessageUpdateView, MessageDeleteView
)


urlpatterns = [
    path('dashboard/', dashboard_patient, name='dashboard'),
    path('appointments/book/', book_appointment, name='book_appointment'),
    path('appointments/', view_appointments, name='view_appointments'),
    path('history/', view_history, name='view_history'),
    path('messages/send/', send_message, name='send_message'),
    path('messages/inbox/', inbox, name='inbox'),
    path('messages/inbox/<int:id>/', inbox_current, name='inbox_current'),
    path('appointments/edit/<int:pk>/', AppointmentUpdateView.as_view(), name='edit_appointment'),
    path('appointments/delete/<int:pk>/', AppointmentDeleteView.as_view(), name='delete_appointment'),
    path('researches/', researches, name='researches'),
    path('feedback/', feedback, name='feedback'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/', profile_view, name='profile'),
    path('survey/', patient_survey, name='patient_survey'),
    path('medical_consent/', medical_consent_view, name='medical_consent'),
    path('order_call/', ordercall, name='order_call'),
]
