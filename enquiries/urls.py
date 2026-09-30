from django.urls import path
from . import views

app_name = 'enquiries'

urlpatterns = [
    path('submit/', views.submit_enquiry_view, name='submit'),
    path('success/', views.success_view, name='success'),
]
