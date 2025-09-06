from django.db import models
from django.utils import timezone

class Event(models.Model):
    EVENT_TYPES = [
        ("ACADEMIC", "Académique"),
        ("SPORT", "Sportif"),
        ("CULTURAL", "Culturel"),
        ("EXTERNAL", "Externe"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default="ACADEMIC")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.get_event_type_display()}"

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()

    @property
    def is_ongoing(self):
        """Retourne True si l'événement est en cours"""
        now = timezone.now()
        return self.start_date <= now <= self.end_date
