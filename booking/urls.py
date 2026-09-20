from django.urls import path
from booking import views

urlpatterns = [
    path('portfolio/', views.booking_portfolio, name='booking_portfolio'),
    path('review/', views.reviews, name='booking_review'),
]