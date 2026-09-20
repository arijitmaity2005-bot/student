from django.db import models

# Create your models here.
class Booking(models.Model):

    event_type = models.CharField(max_length=100)

    event_date = models.DateField()

    event_time = models.TimeField()

    guests = models.PositiveIntegerField()

    budget = models.PositiveIntegerField()

    menu = models.TextField(blank=True)

    location = models.CharField(max_length=100,default="other")

    requirements = models.TextField(blank=True)

    advance_amount = models.PositiveIntegerField(
        default=50000
    )

    booking_status = models.CharField(
        max_length=30,
        default="Confirmed"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.event_type
