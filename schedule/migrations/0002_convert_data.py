from django.db import migrations


def convert_old_data(apps, schema_editor):
    # Récupérer les modèles
    Schedule = apps.get_model('schedule', 'Schedule')
    Filiere = apps.get_model('schedule', 'Filiere')
    Annee = apps.get_model('schedule', 'Annee')
    Salle = apps.get_model('schedule', 'Salle')
    Cours = apps.get_model('schedule', 'Cours')

    # Créer les données de base
    filiere_info, _ = Filiere.objects.get_or_create(nom="Informatique")
    filiere_droit, _ = Filiere.objects.get_or_create(nom="Droit")
    filiere_gestion, _ = Filiere.objects.get_or_create(nom="Gestion")

    annee_l1, _ = Annee.objects.get_or_create(nom="Licence 1")
    annee_l2, _ = Annee.objects.get_or_create(nom="Licence 2")
    annee_l3, _ = Annee.objects.get_or_create(nom="Licence 3")

    salle_a, _ = Salle.objects.get_or_create(nom="Salle A", capacite=30)
    salle_b, _ = Salle.objects.get_or_create(nom="Salle B", capacite=25)
    salle_c, _ = Salle.objects.get_or_create(nom="Salle C", capacite=20)

    # Créer des cours par défaut
    cours_prog, _ = Cours.objects.get_or_create(nom="Programmation Python", filiere=filiere_info)
    cours_droit, _ = Cours.objects.get_or_create(nom="Droit Civil", filiere=filiere_droit)
    cours_gestion, _ = Cours.objects.get_or_create(nom="Comptabilité", filiere=filiere_gestion)


def reverse_convert(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(convert_old_data, reverse_convert),
    ]