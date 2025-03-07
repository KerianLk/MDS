from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
from admin_panel.models import Section, Page
from django.template import Template, Context
from admin_panel.views import *

def dashboard(request):
    return render(request, 'users/dashboard.html')

@login_required
def lk(request):
    if is_admin(request.user):
        return redirect('admin_panel:dashboard')
    if is_patient(request.user):
        return redirect('patient:dashboard')
    if is_doctor(request.user):
        return redirect('doctor:dashboard')
    return render(request, 'users/dashboard.html')

# Главная страница сайта
def index(request):
    sections = Section.objects.all()
    return render(request, 'main/index.html', {'sections': sections})

# Детали раздела
def section_detail(request, section_slug):
    section = get_object_or_404(Section, slug=section_slug)
    pages = section.pages.all()  # Связанные страницы
    return render(request, 'main/section_detail.html', {'section': section, 'pages': pages})

# Детали страницы
def page_detail(request, section_slug, page_slug):
    section = get_object_or_404(Section, slug=section_slug)
    page = get_object_or_404(Page, slug=page_slug, section=section)
    raw_content = page.content
    rendered_conten = Template(raw_content).render(Context({}))
    context = {
        'section': section,
        'page': page,
        'title': page.title,
        'content': page.content,
        'ccc':rendered_conten,
    }
    print(context)
    if page_slug == 'specialists':
        #from .models import Specialist
        #specialists = Specialist.objects.filter(is_active=True)
        context['specialists'] = 'SSSSSSSSSSS'

    return render(request, 'main/page_detail.html', context)
