from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Étudiant'),
        ('admin', 'Administrateur'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def save(self, *args, **kwargs):
        # Si c’est un superuser ou staff → toujours admin
        if self.is_staff or self.is_superuser:
            self.role = "admin"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
