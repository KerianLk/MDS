from django.urls import path
from .views import *

app_name = "main"

urlpatterns = [
#    path('', dashboard, name='dashboard'),
    path('', index, name='index'),
    path('lk', lk, name='lk'),

    # Динамический роутинг для разделов и страниц
    path('<slug:section_slug>/', section_detail, name='section_detail'),
    path('<slug:section_slug>/<slug:page_slug>/', page_detail, name='page_detail'),
]
