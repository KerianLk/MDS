from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("sections/", views.section_list, name="section_list"),
    path("sections/add/", views.add_section, name="add_section"),
    path("sections/<int:pk>/edit/", views.edit_section, name="edit_section"),
    path("sections/<int:pk>/delete/", views.delete_section, name="delete_section"),
    path("pages/", views.page_list, name="page_list"),
    path("pages/add/", views.add_page, name="add_page"),
    path("pages/<int:pk>/edit/", views.edit_page, name="edit_page"),
    path("pages/<int:pk>/delete/", views.delete_page, name="delete_page"),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/<int:pk>/', views.feedback_detail, name='feedback_detail'),
    path('feedback/<int:pk>/accept/', views.feedback_accept, name='feedback_accept'),
    path('feedback/<int:pk>/delete/', views.feedback_delete, name='feedback_delete'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
]
