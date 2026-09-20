from django.shortcuts import render
from .models import Booking


def booking(request):

    if request.method == "POST":

        event_type = request.POST.get("event_type")

        event_date = request.POST.get("event_date")

        event_time = request.POST.get("event_time")

        guests = request.POST.get("guests")

        budget = request.POST.get("budget")

        location = request.POST.get("location")

        requirements = request.POST.get("requirements")


        # Multiple menu items
        menu_items = request.POST.getlist("menu")

        menu = ", ".join(menu_items)


        # Fixed advance payment
        advance_amount = 50000


        # Save booking

        booking = Booking.objects.create(

            event_type=event_type,

            event_date=event_date,

            event_time=event_time,

            guests=guests,

            budget=budget,

            menu=menu,
            
            location=location,

            requirements=requirements,

            advance_amount=advance_amount,

            booking_status="Confirmed"

        )


        return render(
            request,
            "booking_confirmation.html",
            {
                "booking": booking
            }
        )


    return render(
        request,
        "booking.html"
    )