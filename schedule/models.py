from django.db import models


# Modèles de configuration admin
class Filiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Cours(models.Model):
    nom = models.CharField(max_length=200)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.filiere.nom})"


class Salle(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    capacite = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Annee(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


# Modèle principal Schedule - VERSION FINALE SANS ANCIENS CHAMPS
class Schedule(models.Model):
    DAY_CHOICES = (
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
        ('samedi', 'Samedi'),
    )

    # Relations flexibles - VERSION FINALE
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    annee = models.ForeignKey(Annee, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)

    # Informations horaires
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    professeur = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.cours.nom} - {self.filiere.nom} {self.annee.nom} - {self.day} {self.start_time}"