from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('search-suggestions/', views.product_search_suggestions_view, name='search_suggestions'),
    path('redirect/<int:link_id>/', views.marketplace_redirect_view, name='marketplace_redirect'),
    path('<slug:slug>/', views.product_detail_view, name='product_detail'),
]
