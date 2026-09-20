from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='home'),
    path('confirm_booking/', views.booking, name='booking'),
]