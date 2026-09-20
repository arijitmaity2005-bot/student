from django.shortcuts import render


def cancel_booking(request):
    return render(request, 'cancel_booking.html')