from django.shortcuts import render

# Create your views here.
#def booking_view(request):
    #return render(request, 'booking.html')
def booking_portfolio(request):
    return render(request, 'portfolio.html')
def reviews(request):
    return render(request, 'review.html')
