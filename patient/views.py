from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import UpdateView, DeleteView

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from admin_panel.views import *
from datetime import datetime, time
from django.db.models import Q

from datetime import datetime, time, timedelta



def generate_time_slots(start_time, end_time, interval_minutes):
    slots = []
    current_time = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)

    while current_time < end_datetime:
        slots.append(current_time.time())
        current_time += timedelta(minutes=interval_minutes)
    return slots

def get_available_slots(date, specialist):
    booked_slots = Appointment.objects.filter(date=date, doctor=specialist).values_list('time', flat=True)
    all_slots = generate_time_slots(time(9, 0), time(20, 0), 30)
    available_slots = [slot for slot in all_slots if slot not in booked_slots]
    return available_slots


@user_passes_test(is_patient,login_url='/lk')
def dashboard_patient(request):
    zapisi = Appointment.objects.all()
    for z in zapisi:
        combined_datetime = datetime.combine(z.date, z.time)
        now = datetime.now()
        if combined_datetime < now:
            z.status = 'success'
        z.save()
    return render(request, 'patients/index.html')


@user_passes_test(is_patient,login_url='/lk')
def book_appointment(request):
    #if is_patient(request.user):
    #    return redirect('dashboard')  # только пациенты могут записываться
    available_slots = []
    if request.method == 'POST':
        form = AppointmentFormPatient(request.POST, available_slots=available_slots)
        if form.is_valid():
            appointment = form.save(commit=False)
            print(request.user)
            appointment.patient = request.user
            appointment.save()
            return redirect('patient:view_appointments')
    else:
        date = request.GET.get('date')
        specialist = request.GET.get('doctor')
        #specialist = 1
        #date = '2025-01-01'
        if date and specialist:
            available_slots = get_available_slots(date, specialist)

        form = AppointmentFormPatient(available_slots=available_slots)
        print(form)
    return render(request, 'patients/book_appointment.html', {'form': form})

@user_passes_test(is_patient,login_url='/lk')
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
    appointments = Appointment.objects.filter(patient=request.user,status='wait').order_by(sort_by)
    #appointments = Appointment.objects.filter(patient=request.user,status='wait')
    return render(request, 'patients/view_appointments.html', {'appointments': appointments})

@user_passes_test(is_patient,login_url='/lk')
def view_history(request):
    history =  Appointment.objects.filter(patient=request.user,status='success')
    return render(request, 'patients/view_history.html', {'history': history})

@user_passes_test(is_patient,login_url='/lk')
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST,current_user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('patient:inbox')
    else:
        form = MessageForm(current_user=request.user)
    return render(request, 'patients/send_message.html', {'form': form})

@user_passes_test(is_patient,login_url='/lk')
def inbox(request):
    messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    doctors = User.objects.filter(Q(role='doctor') | Q(role='admin'))
    return render(request, 'patients/inbox.html', {'messages': messages,'doctors':doctors})

@user_passes_test(is_patient,login_url='/lk')
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
            return redirect('patient:inbox_current',id)
    else:
        # Передаем начальное значение для receiver
        initial_data = {
            'receiver': user.id  # Автоматически подставляем текущего пользователя как получателя
        }
        form = MessageForm(current_user=request.user, initial=initial_data)
        #form = MessageForm(current_user=request.user)
    return render(request, 'patients/inbox.html', {'messages': messages, 'form':form})


@user_passes_test(is_patient,login_url='/lk')
def researches(request):
    messages = MedicalRecord.objects.filter(patient=request.user)
    return render(request, 'patients/researches.html', {'messages': messages})


@user_passes_test(is_patient,login_url='/lk')
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
            return redirect('patient:dashboard')
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
class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'patients/delete_appointment.html'
    success_url = reverse_lazy('patient:view_appointments')

    def get_queryset(self):
        # Ограничение для текущего пациента
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


from django.shortcuts import render, redirect
from .forms import UserProfileForm, UserDataForm
from .models import UserProfile

@user_passes_test(is_patient,login_url='/lk')
def edit_profile(request):
    #profile, created = UserProfile.objects.get_or_create(user=request.user)
    user = request.user
    #profile = UserProfile.objects.get_or_create(user=user)
    profile = get_object_or_404(UserProfile, user=user)
    if request.method == 'POST':
        user_form = UserDataForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            # Сохраняем данные модели UserProfile
            profile_form.save()
            return redirect('patient:profile')  # Перенаправить на страницу профиля
    else:
        user_form = UserDataForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    return render(request, 'patients/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@user_passes_test(is_patient,login_url='/lk')
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    #user_profile = get_object_or_404(UserProfile, user=request.user)
    user = request.user
    user_profile = user.profile  # Доступ к UserProfile через related_name
    return render(request, 'patients/profile.html', {
        'user': user,
        'profile': user_profile,
    })


from .forms import PatientSurveyForm
from .models import PatientSurvey

@user_passes_test(is_patient,login_url='/lk')
def patient_survey(request):
    survey, created = PatientSurvey.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PatientSurveyForm(request.POST, instance=survey)
        if form.is_valid():
            survey.completed = True
            form.save()
            return redirect('patient:profile')  # Перенаправить на главную
    else:
        form = PatientSurveyForm(instance=survey)
    return render(request, 'patients/patient_survey.html', {'form': form})

@user_passes_test(is_patient,login_url='/lk')
def medical_consent_view(request):
    sogl = MedicalConsent.objects.get_or_create(user=request.user)
    soglasie = get_object_or_404(MedicalConsent, user=request.user)
    if request.method == 'POST':
        form = MedicalConsentForm(request.POST, request.FILES, instance=soglasie)
        if form.is_valid():
            consent = form.save(commit=False)
            consent.user = request.user  # Привязываем к текущему пользователю
            consent.save()
            return redirect('patient:dashboard')  # Перенаправление после успешного сохранения
    else:
        form = MedicalConsentForm(instance=soglasie)

    return render(request, 'patients/medical_consent.html', {'form': form})

@user_passes_test(is_patient,login_url='/lk')
def ordercall(request):
    if request.method == 'POST':
        form = OrderCallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient:dashboard')  # Перенаправление после успешного сохранения
    else:
        form = OrderCallForm()

    return render(request, 'patients/ordercall.html', {'form': form})