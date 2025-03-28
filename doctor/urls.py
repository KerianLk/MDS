from django.urls import path
from .views import *

app_name = "doctor"

urlpatterns = [
    path('dashboard/', view_appointments, name='dashboard'),
    path('appointments/book/', book_appointment, name='book_appointment'),
    path('appointments/', view_appointments, name='view_appointments'),
    path('history/<int:id>/', view_history, name='view_history'),
    path('messages/send/', send_message, name='send_message'),
    path('messages/send/<int:id>/', send_message_to_patient, name='send_message_to_patient'),
    path('messages/inbox/', inbox, name='inbox'),
    path('messages/inbox/<int:id>/', inbox_current, name='inbox_current'),
    path('appointments/edit/<int:pk>/', AppointmentUpdateView.as_view(), name='edit_appointment'),
    path('appointments/delete/<int:pk>/', AppointmentDoctorDeleteView.as_view(), name='delete_appointment'),
    path('researches/', researches, name='researches'),
    path('feedback/', feedback, name='feedback'),
]