from django.urls import path
from contactus import views

urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
]