from django.urls import path
from . import views

urlpatterns = [
    path('', views.cancel_booking, name='cancel_booking'),
]