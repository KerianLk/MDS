from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import UpdateView, DeleteView
from time import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from admin_panel.views import *
from datetime import datetime, time
from django.db.models import Q
from datetime import datetime, time
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect

from datetime import datetime, time, timedelta




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
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user

            # Проверка даты
            today = datetime.today().date()
            if appointment.date < today:
                form.add_error('date', 'Дата не может быть в прошлом!')
                return render(request, 'patients/book_appointment.html', {'form': form})

            # Проверка времени
            start_time = time(9, 0)  # 9:00
            end_time = time(18, 0)  # 18:00
            if not (start_time <= appointment.time <= end_time):
                form.add_error('time', 'Время должно быть между 9:00 и 18:00!')
                return render(request, 'patients/book_appointment.html', {'form': form})

            # Сохраняем запись, если валидация прошла
            appointment.save()

            # Подготовка и отправка письма
            subject = "Новая заявка на запись"
            message = (
                f"Новая заявка на запись создана.\n\n"
                f"ДАТА ПРИЕМА: {appointment.date}\n"
                f"ВРЕМЯ: {appointment.time}\n"
                f"СПЕЦИАЛИСТ: {appointment.doctor}\n"
                f"ЦЕЛЬ ВИЗИТА: {appointment.usluga}\n"
                "Поесть за 1–2 часа до приёма. Еда должна быть в меру калорийной и достаточно сытной. Нежелательно приходить к стоматологу натощак: из-за этого выделение слюны будет обильным, возможно ухудшение самочувствия.\n"
                "Не принимать алкоголь накануне и в день визита к врачу. Спиртное может влиять на состояние слизистых и снижать эффективность анестезии.\n"
                "Почистить зубы незадолго до визита. Для этого нужно воспользоваться зубной щёткой и нитью, прополоскать рот водой.\n"
                "Воздержаться от приёма медикаментов перед визитом. Они могут снизить действие местной анестезии. О любых принятых за последние сутки лекарственных препаратах нужно сообщить врачу до начала лечения.\n"
                "Взять с собой документы. При первом посещении потребуется гражданский паспорт. Если есть снимки зубов, направления других врачей или результаты выполненных недавно общих анализов, их тоже стоит взять с собой.\n"
                "Подготовиться к вопросам. Врач будет задавать вопросы о наличии заболеваний, проблем, аллергии. В личном кабинете вы можете указать, на какие вещества и препараты имеется аллергическая реакция.\n"
                "Если перед посещением врача обострилось какое-либо хроническое заболевание, желательно позвонить врачу и уточнить, возможно ли посещение.\n"
                "В описании услуг вы можете ознакомиться со всеми рекомендациями и особенностями вашего визита.\n\n"
            )
            html_message = (
                f"Новая заявка на запись создана.<br>"
                f"ДАТА ПРИЕМА: {appointment.date}<br>"
                f"ВРЕМЯ: {appointment.time}<br>"
                f"СПЕЦИАЛИСТ: {appointment.doctor}<br>"
                f"ЦЕЛЬ ВИЗИТА: {appointment.usluga}<br>"
                 "Поесть за 1–2 часа до приёма. Еда должна быть в меру калорийной и достаточно сытной. Нежелательно приходить к стоматологу натощак: из-за этого выделение слюны будет обильным, возможно ухудшение самочувствия.<br>"
    "Не принимать алкоголь накануне и в день визита к врачу. Спиртное может влиять на состояние слизистых и снижать эффективность анестезии.<br>"
    "Почистить зубы незадолго до визита. Для этого нужно воспользоваться зубной щёткой и нитью, прополоскать рот водой.<br>"
    "Воздержаться от приёма медикаментов перед визитом. Они могут снизить действие местной анестезии. О любых принятых за последние сутки лекарственных препаратах нужно сообщить врачу до начала лечения.<br>"
    "Взять с собой документы. При первом посещении потребуется гражданский паспорт. Если есть снимки зубов, направления других врачей или результаты выполненных недавно общих анализов, их тоже стоит взять с собой.<br>"
    "Подготовиться к вопросам. Врач будет задавать вопросы о наличии заболеваний, проблем, аллергии. В личном кабинете вы можете указать, на какие вещества и препараты имеется аллергическая реакция.<br>"
    "Если перед посещением врача обострилось какое-либо хроническое заболевание, желательно позвонить врачу и уточнить, возможно ли посещение.<br>"
    "В описании услуг вы можете ознакомиться со всеми рекомендациями и особенностями вашего визита.<br><br>"
    '<a href="https://example.com">ПЕРЕЙТИ</a>'
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            # Предполагается, что у модели доктора есть поле email.
            #recipient_list = [appointment.doctor.email,appointment.patient.email]
            recipient_list = [appointment.patient.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False,html_message=html_message)

            return redirect('patient:view_appointments')
    else:
        form = AppointmentForm()

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

    # Получение всех записей пациента
    appointments = Appointment.objects.filter(patient=request.user, status='wait').order_by(sort_by)

    # Перевод просроченных записей в историю
    now = datetime.now().time()  # Текущее время
    today = datetime.now().date()  # Текущая дата

    for appointment in appointments:
        # Если запись просрочена (дата меньше текущей, или дата та же, но время прошло)
        if appointment.date < today or (appointment.date == today and appointment.time < now):
            appointment.status = 'success'  # Обновляем статус
            appointment.save()  # Сохраняем изменения

    return render(request, 'patients/view_appointments.html', {'appointments': appointments})

@user_passes_test(is_patient,login_url='/lk')
def view_history(request):
    history =  Appointment.objects.filter(patient=request.user,status='success')
    return render(request, 'patients/view_history.html', {'history': history})

@user_passes_test(is_patient,login_url='/lk')
def send_message(request):
    users = User.objects.filter(role='doctor')
    if request.method == 'POST':
        form = MessageForm(request.POST,current_user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('patient:inbox')
    else:
        form = MessageForm(current_user=request.user)
    return render(request, 'patients/send_message.html', {'form': form, 'doctors' : users})

@user_passes_test(is_patient,login_url='/lk')
def send_message_to_doctor(request, id):
    users = User.objects.filter(role='doctor')
    doctor = User.objects.filter(id=id)
    messages = Message.objects.filter((Q(sender=request.user) & Q(receiver=doctor[0])) | (Q(sender=doctor[0]) & Q(receiver=request.user))).order_by('created_at')
    if request.method == 'POST':
        form = MessageForm(request.POST,current_user=request.user)
        if form.is_valid():
            print("OK")
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('patient:send_message_to_doctor', id)
    else:
        form = MessageForm(current_user=request.user)
    return render(request, 'patients/send_message.html', {'form': form, 'doctors' : users, 'id' : id, 'current_doctor' : doctor, 'messages' : messages})

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
    user = request.user
    user_profile = user.profile
    if request.method == 'POST':
        form = PatientSurveyForm(request.POST, instance=survey)
        if form.is_valid():
            survey.completed = True
            form.save()
            return redirect('patient:profile')  # Перенаправить на главную
    else:
        form = PatientSurveyForm(instance=survey)
    return render(request, 'patients/patient_survey.html', {'form': form, 'user': user, 'profile': user_profile, 'survey': survey})

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