from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('page/<slug:slug>/', views.page_detail_view, name='page_detail'),
    path('robots.txt', views.robots_view, name='robots'),
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
    path('health/', views.health_check_view, name='health_check'),
]

