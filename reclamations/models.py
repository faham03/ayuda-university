from django.db import models
from django.conf import settings
from grades.models import Grade  # on relie à la note

class Reclamation(models.Model):
    STATUS_CHOICES = (
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('rejettee', 'Rejetée'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reclamations"
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name="reclamations"
    )
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='en_attente'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "grade", "status")
        # Cela empêche qu’un étudiant fasse plusieurs réclamations EN ATTENTE
        # pour la même note

    def __str__(self):
        return f"Réclamation {self.id} - {self.student.username} ({self.status})"
