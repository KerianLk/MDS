from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Section, Page
from .forms import SectionForm, PageForm
from django.contrib import messages
from patient.models import Feedback, Appointment
from users.models import User
from django.contrib.auth.hashers import make_password
from .forms import UserForm, AppointmentForm

def is_admin(user):
    return user.is_authenticated and user.role == "admin"

def is_patient(user):
    return user.is_authenticated and user.role == "patient"

def is_doctor(user):
    return user.is_authenticated and user.role == "doctor"




@user_passes_test(is_admin)
def dashboard(request):
    return render(request, "admin_panel/dashboard.html")

@login_required
@user_passes_test(is_admin)
def section_list(request):
    sections = Section.objects.all()
    return render(request, "admin_panel/section_list.html", {"sections": sections})

@login_required
@user_passes_test(is_admin)
def add_section(request):
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:section_list")
    else:
        form = SectionForm()
    return render(request, "admin_panel/add_section.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def edit_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:section_list")
    else:
        form = SectionForm(instance=section)
    return render(request, "admin_panel/edit_section.html", {"form": form, "section": section})

@login_required
@user_passes_test(is_admin)
def delete_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    section.delete()
    return redirect("admin_panel:section_list")

@login_required
@user_passes_test(is_admin)
def page_list(request):
    pages = Page.objects.select_related("section").all()
    return render(request, "admin_panel/page_list.html", {"pages": pages})

@login_required
@user_passes_test(is_admin)
def add_page(request):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:page_list")
    else:
        form = PageForm()
    return render(request, "admin_panel/add_page.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def edit_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == "POST":
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:page_list")
    else:
        form = PageForm(instance=page)
    return render(request, "admin_panel/edit_page.html", {"form": form, "page": page})

@login_required
@user_passes_test(is_admin)
def delete_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    page.delete()
    return redirect("admin_panel:page_list")

@user_passes_test(is_admin)
def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/feedback_list.html', {'feedbacks': feedbacks})

@user_passes_test(is_admin)
def feedback_detail(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    return render(request, 'admin_panel/feedback_detail.html', {'feedback': feedback})

@user_passes_test(is_admin)
def feedback_accept(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.status = True
    feedback.save()
    messages.success(request, "Отзыв успешно принят.")
    return redirect('admin_panel:feedback_list')

@user_passes_test(is_admin)
def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.delete()
    messages.success(request, "Отзыв успешно удален.")
    return redirect('admin_panel:feedback_list')

@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/user_list.html', {'users': users})

@user_passes_test(is_admin)
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'admin_panel/user_detail.html', {'user': user})

@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Пользователь успешно добавлен.")
            return redirect('admin_panel:user_list')
    else:
        form = UserForm()
    return render(request, 'admin_panel/user_form.html', {'form': form})

@user_passes_test(is_admin)
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Пользователь успешно обновлен.")
            return redirect('admin_panel:user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'admin_panel/user_form.html', {'form': form})

@user_passes_test(is_admin)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, "Пользователь успешно удален.")
    return redirect('admin_panel:user_list')


@user_passes_test(is_admin)
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/appointment_list.html', {'appointments': appointments})

@user_passes_test(is_admin)
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'admin_panel/appointment_detail.html', {'appointment': appointment})

@user_passes_test(is_admin)
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно создана.")
            return redirect('admin_panel:appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'admin_panel/appointment_form.html', {'form': form})

@user_passes_test(is_admin)
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно обновлена.")
            return redirect('admin_panel:appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'admin_panel/appointment_form.html', {'form': form})

@user_passes_test(is_admin)
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, "Запись успешно удалена.")
    return redirect('admin_panel:appointment_list')