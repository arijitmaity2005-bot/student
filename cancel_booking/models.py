from django.db import models


class Booking(models.Model):

    EVENT_TYPES = [
        ("Wedding", "Wedding"),
        ("Birthday", "Birthday Party"),
        ("Engagement", "Engagement"),
        ("Anniversary", "Anniversary"),
        ("Corporate", "Corporate Event"),
        ("Cultural", "Cultural Program"),
        ("Workshop", "Workshop"),
    ]

    LOCATIONS = [
        ("kolkata", "Kolkata"),
        ("durgapur", "Durgapur"),
        ("siliguri", "Siliguri"),
        ("howrah", "Howrah"),
        ("kharagpur", "Kharagpur"),
        ("other", "Other"),
    ]

    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPES
    )

    event_date = models.DateField()

    event_time = models.TimeField()

    guests = models.PositiveIntegerField()

    budget = models.PositiveIntegerField()

    menu = models.JSONField(default=list)

    location = models.CharField(
        max_length=30,
        choices=LOCATIONS
    )

    requirements = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default="Confirmed"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Booking #{self.id} - {self.event_type}"