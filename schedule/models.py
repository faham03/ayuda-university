from django.db import models
from django.apps import apps
import datetime

class Schedule(models.Model):
    FILIERE_CHOICES = (
        ('informatique', 'Informatique'),
        ('droit', 'Droit'),
        ('gestion', 'Gestion'),
    )

    YEAR_CHOICES = (
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
    )

    DAY_CHOICES = (
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
        ('samedi', 'Samedi'),
    )

    SALLE_CHOICES = (
        ('Salle A', 'Salle A'),
        ('Salle B', 'Salle B'),
        ('Salle C', 'Salle C'),
        ('Salle D', 'Salle D'),
    )

    filiere = models.CharField(max_length=20, choices=FILIERE_CHOICES)
    year = models.CharField(max_length=5, choices=YEAR_CHOICES)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    course_name = models.CharField(max_length=100)
    professeur = models.CharField(max_length=100, null=True, blank=True)
    salle = models.CharField(max_length=20, choices=SALLE_CHOICES, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.filiere} {self.year} - {self.day}: {self.course_name} ({self.salle})"


def check_conflicts(course):
    """Vérifie si un cours entre en conflit avec un événement académique"""
    Event = apps.get_model('events', 'Event')  # Récupération dynamique du modèle
    conflicts = Event.objects.filter(
        location=course.salle,
        start_date__lt=datetime.datetime.combine(datetime.date.today(), course.end_time),
        end_date__gt=datetime.datetime.combine(datetime.date.today(), course.start_time),
        event_type="ACADEMIC"
    )
    return conflicts.exists()
