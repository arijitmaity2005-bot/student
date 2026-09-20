from django.urls import path
from login import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_view, name='register'),
    path('register/submit/', views.register_user, name='register_user'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('logout/', views.logout_user, name='logout'),
]