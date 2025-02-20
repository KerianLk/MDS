from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import UpdateView, DeleteView

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from patient.models import Appointment, MedicalRecord, Message
from patient.forms import *
from admin_panel.views import *
from datetime import datetime, time
from .forms import *
from django.db.models import Q

@user_passes_test(is_doctor,login_url='/lk')
def dashboard_doctor(request):
    zapisi = Appointment.objects.all()
    for z in zapisi:
        combined_datetime = datetime.combine(z.date, z.time)
        now = datetime.now()
        if combined_datetime < now:
            z.status = 'success'
        z.save()
    return render(request, 'doctor/dashboard.html')





@user_passes_test(is_doctor,login_url='/lk')
def book_appointment(request):
    #if is_patient(request.user):
    #    return redirect('dashboard')  # только пациенты могут записываться
    if request.method == 'POST':
        form = AppointmentFormDoctor(request.POST)
        print(form.is_valid)
        if form.is_valid():
            appointment = form.save(commit=False)
            print(request.user)
            appointment.doctor = request.user
            appointment.save()
            return redirect('patient:view_appointments')
    else:
        form = AppointmentFormDoctor()
    return render(request, 'patients/book_appointment.html', {'form': form})

@user_passes_test(is_doctor,login_url='/lk')
def view_appointments(request):
    sort_by = request.GET.get('sort_by', 'date_added')  # Получение параметра сортировки
    order = request.GET.get('order', 'asc')  # Порядок сортировки: asc или desc
    # Выбор поля сортировки
    if sort_by not in ['date', 'patient']:
        sort_by = 'date'
    # Применение порядка сортировки
    if order == 'desc':
        sort_by = f"-{sort_by}"
    # Получение отсортированных записей
    appointments = Appointment.objects.filter(doctor=request.user,status='wait').order_by(sort_by)
    #appointments = Appointment.objects.filter(patient=request.user,status='wait')
    return render(request, 'doctor/view_appointments.html', {'appointments': appointments})

@user_passes_test(is_doctor,login_url='/lk')
def view_history(request,id):
    print(id)
    history =  Appointment.objects.filter(patient_id=id,status='success')

    return render(request, 'doctor/view_history.html', {'history': history})

@user_passes_test(is_doctor,login_url='/lk')
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST,current_user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('doctor:inbox')
    else:
        form = MessageForm(current_user=request.user)
    return render(request, 'patients/send_message.html', {'form': form})

@user_passes_test(is_doctor,login_url='/lk')
def inbox(request):
#    messages = (Message.objects.filter(sender=request.user) or Message.objects.filter(receiver=request.user))
    messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))

    patient = User.objects.filter(role='patient')
    return render(request, 'patients/inbox.html', {'messages': messages, 'patient': patient})

@user_passes_test(is_doctor,login_url='/lk')
def inbox_current(request,id):
    user = User.objects.get(id=id)
#    messages = Message.objects.filter(sender=request.user) or Message.objects.filter(receiver=request.user)\
#        or Message.objects.filter(sender=user.id) or Message.objects.filter(receiver=user.id)
    messages = Message.objects.filter(Q(sender=request.user) & Q(receiver=user.id) | Q(sender=user.id) & Q(receiver=request.user)).order_by('created_at')
    if request.method == 'POST':
        form = MessageForm(request.POST, current_user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('doctor:inbox_current',id)
    else:
        # Передаем начальное значение для receiver
        initial_data = {
            'receiver': user.id  # Автоматически подставляем текущего пользователя как получателя
        }
        form = MessageForm(current_user=request.user, initial=initial_data)
        #form = MessageForm(current_user=request.user)
    return render(request, 'patients/inbox.html', {'messages': messages, 'form':form})

@user_passes_test(is_doctor,login_url='/lk')
def researches(request):
    messages = MedicalRecord.objects.filter(doctor=request.user)
    return render(request, 'patients/researches.html', {'messages': messages})


@user_passes_test(is_doctor,login_url='/lk')
def feedback(request):
    #if is_patient(request.user):
    #    return redirect('dashboard')  # только пациенты могут записываться
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            print(request.user)
            appointment.patient = request.user
            appointment.save()
            return redirect('doctor:dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'patients/feedback.html', {'form': form})


# Редактирование записи на прием
class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ['doctor', 'date', 'time']
    template_name = 'patients/edit_appointment.html'
    success_url = reverse_lazy('patient:view_appointments')

    def get_queryset(self):
        # Ограничение для текущего пациента
        return Appointment.objects.filter(patient=self.request.user)

# Удаление записи на прием
class AppointmentDoctorDeleteView(DeleteView):
    model = Appointment
    template_name = 'patients/delete_appointment.html'
    success_url = reverse_lazy('doctor:view_appointments')

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)

# Редактирование сообщения
class MessageUpdateView(UpdateView):
    model = Message
    fields = ['receiver', 'subject', 'body']
    template_name = 'patients/edit_message.html'
    success_url = reverse_lazy('inbox')

    def get_queryset(self):
        # Только отправленные пользователем сообщения
        return Message.objects.filter(sender=self.request.user)

# Удаление сообщения
class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'patients/delete_message.html'
    success_url = reverse_lazy('inbox')

    def get_queryset(self):
        # Только отправленные пользователем сообщения
        return Message.objects.filter(sender=self.request.user)



