from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html')


def index(request):
    return render(request, 'index.html')


def reviews(request):
    return render(request, 'review.html')


def services(request):
    return render(request, 'services.html')


def portfolio(request):
    return render(request, 'portfolio.html')


def reason(request):
    return render(request, 'reason.html')
    