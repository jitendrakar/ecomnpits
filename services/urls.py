from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list_view, name='service_list'),
    path('cctv-calculator/', views.cctv_calculator_view, name='cctv_calculator'),
    path('<slug:slug>/', views.service_detail_view, name='service_detail'),
]
