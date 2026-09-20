from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.index, name='index'),
    path('reviews/', views.reviews, name='reviews'),
    path('services/', views.services, name='services'),
    path('services.html', views.services, name='services_html'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio.html', views.portfolio, name='portfolio_html'),
    path('reason/', views.reason, name='reason'),
    path('reason.html', views.reason, name='reason_html'),
]