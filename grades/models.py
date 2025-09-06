from django.db import models
from django.conf import settings

class Grade(models.Model):
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

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grades')
    filiere = models.CharField(max_length=20, choices=FILIERE_CHOICES)
    year = models.CharField(max_length=5, choices=YEAR_CHOICES)
    subject = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)  # par ex. 18.50
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'year', 'filiere')  # empêche doublons

    def __str__(self):
        return f"{self.student.username} - {self.subject} : {self.score}"
