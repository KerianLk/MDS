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
from datetime import datetime, time
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect

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
    if request.method == 'POST':
        form = AppointmentFormDoctor(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = request.user  # Доктор назначает запись

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
            # recipient_list = [appointment.doctor.email,appointment.patient.email]
            recipient_list = [appointment.patient.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)


            return redirect('patient:view_appointments')

    else:
        form = AppointmentFormDoctor()

    return render(request, 'patients/book_appointment.html', {'form': form})

@user_passes_test(is_doctor,login_url='/lk')
def view_appointments(request):
    # Получаем текущую дату и время
    now = datetime.now()

    # Обновление статуса для просроченных записей
    appointments_to_update = Appointment.objects.filter(doctor=request.user, status='wait', date__lt=now.date())
    for appointment in appointments_to_update:
        # Если время записи уже прошло (сравниваем время)
        if appointment.date < now.date() or (appointment.date == now.date() and appointment.time < now.time()):
            appointment.status = 'success'
            appointment.save()

    # Сортировка по параметрам
    sort_by = request.GET.get('sort_by', 'date_added')  # Получение параметра сортировки
    order = request.GET.get('order', 'asc')  # Порядок сортировки: asc или desc

    if sort_by not in ['date', 'patient']:
        sort_by = 'date'
    if order == 'desc':
        sort_by = f"-{sort_by}"

    # Получение отсортированных записей
    appointments = Appointment.objects.filter(doctor=request.user, status='wait').order_by(sort_by)

    return render(request, 'doctor/view_appointments.html', {'appointments': appointments})

@user_passes_test(is_doctor,login_url='/lk')
def view_history(request, id):
    # Получение истории записей для пациента с id
    history = Appointment.objects.filter(patient_id=id, status='success', doctor=request.user)

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
    users = User.objects.filter(role='patient')
    if request.method == 'POST':
        form = MessageForm(request.POST,current_user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('doctor:inbox')
    else:
        form = MessageForm(current_user=request.user)
    return render(request, 'doctor/send_message.html', {'form': form, 'doctors' : users})
    #messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))

    #patient = User.objects.filter(role='patient')
    #return render(request, 'patients/inbox.html', {'messages': messages, 'patient': patient})

@user_passes_test(is_doctor,login_url='/lk')
def send_message_to_patient(request, id):
    users = User.objects.filter(role='patient')
    doctor = User.objects.filter(id=id)

    messages = Message.objects.filter((Q(sender=request.user) & Q(receiver=doctor[0])) | (Q(sender=doctor[0]) & Q(receiver=request.user))).order_by('created_at')
    if request.method == 'POST':
        form = MessageForm(request.POST,current_user=request.user)
        if form.is_valid():
            print("OK")
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('doctor:send_message_to_patient', id)
    else:
        form = MessageForm(current_user=request.user)
    return render(request, 'doctor/send_message.html', {'form': form, 'doctors' : users, 'id' : id, 'current_doctor' : doctor, 'messages' : messages})


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