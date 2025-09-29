from rest_framework import serializers
from .models import Filiere, Cours, Salle, Annee, Schedule
import datetime


# Serializers pour la configuration
class FiliereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = ['id', 'nom', 'created_at']


class CoursSerializer(serializers.ModelSerializer):
    filiere_nom = serializers.CharField(source='filiere.nom', read_only=True)

    class Meta:
        model = Cours
        fields = ['id', 'nom', 'filiere', 'filiere_nom', 'created_at']


class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = ['id', 'nom', 'capacite', 'created_at']


class AnneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annee
        fields = ['id', 'nom', 'created_at']


# Serializer principal avec validations améliorées
class ScheduleSerializer(serializers.ModelSerializer):
    filiere_nom = serializers.CharField(source='filiere.nom', read_only=True)
    annee_nom = serializers.CharField(source='annee.nom', read_only=True)
    cours_nom = serializers.CharField(source='cours.nom', read_only=True)
    salle_nom = serializers.CharField(source='salle.nom', read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'filiere', 'filiere_nom', 'annee', 'annee_nom',
            'cours', 'cours_nom', 'salle', 'salle_nom', 'day',
            'start_time', 'end_time', 'professeur', 'created_at'
        ]

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        salle = data.get('salle')
        day = data.get('day')

        # === 1. VALIDATION HEURES MIN/MAX ===
        HEURE_OUVERTURE = datetime.time(7, 0)  # 7h00
        HEURE_FERMETURE = datetime.time(22, 0)  # 22h00

        if start_time < HEURE_OUVERTURE:
            raise serializers.ValidationError(
                f"Les cours ne peuvent pas commencer avant {HEURE_OUVERTURE.strftime('%Hh%M')}"
            )

        if end_time > HEURE_FERMETURE:
            raise serializers.ValidationError(
                f"Les cours ne peuvent pas finir après {HEURE_FERMETURE.strftime('%Hh%M')}"
            )

        # === 2. VALIDATION DÉBUT < FIN ===
        if start_time >= end_time:
            raise serializers.ValidationError("L'heure de début doit être avant l'heure de fin.")

        # === 3. VALIDATION DURÉE ===
        duration = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.combine(
            datetime.date.today(), start_time)
        duration_minutes = duration.total_seconds() / 60

        # Durée minimale : 1 heure
        if duration_minutes < 60:
            raise serializers.ValidationError("Un cours doit durer au moins 1 heure.")

        # Durée maximale : 4 heures
        if duration_minutes > 240:
            raise serializers.ValidationError("Un cours ne peut pas durer plus de 4 heures.")

        # === 4. VALIDATION CONFLITS SALLE (même créneau) ===
        if self.instance:  # Mode modification
            conflicts = Schedule.objects.filter(day=day, salle=salle).exclude(id=self.instance.id)
        else:  # Mode création
            conflicts = Schedule.objects.filter(day=day, salle=salle)

        for conflict in conflicts:
            # Vérifier chevauchement direct
            if (start_time < conflict.end_time and end_time > conflict.start_time):
                raise serializers.ValidationError(
                    f"🚨 CONFLIT DE SALLE !\n"
                    f"La salle {salle.nom} est déjà occupée le {day} par :\n"
                    f"• {conflict.cours.nom} ({conflict.professeur})\n"
                    f"• De {conflict.start_time.strftime('%Hh%M')} à {conflict.end_time.strftime('%Hh%M')}"
                )

        # === 5. VALIDATION PAUSE ENTRE COURS (30 minutes) ===
        PAUSE_OBLIGATOIRE = datetime.timedelta(minutes=30)

        for existing_course in Schedule.objects.filter(day=day, salle=salle):
            if self.instance and existing_course.id == self.instance.id:
                continue  # Ignorer le cours en cours de modification

            # Pause après un cours existant
            time_after_previous = datetime.datetime.combine(datetime.date.today(),
                                                            start_time) - datetime.datetime.combine(
                datetime.date.today(), existing_course.end_time)
            if datetime.timedelta(minutes=0) < time_after_previous < PAUSE_OBLIGATOIRE:
                raise serializers.ValidationError(
                    f"⏰ PAUSE INSUFFISANTE !\n"
                    f"Respectez 30 minutes de pause après le cours :\n"
                    f"• {existing_course.cours.nom} (fini à {existing_course.end_time.strftime('%Hh%M')})\n"
                    f"• Votre cours commence à {start_time.strftime('%Hh%M')}"
                )

            # Pause avant un cours existant
            time_before_next = datetime.datetime.combine(datetime.date.today(),
                                                         existing_course.start_time) - datetime.datetime.combine(
                datetime.date.today(), end_time)
            if datetime.timedelta(minutes=0) < time_before_next < PAUSE_OBLIGATOIRE:
                raise serializers.ValidationError(
                    f"⏰ PAUSE INSUFFISANTE !\n"
                    f"Respectez 30 minutes de pause avant le cours :\n"
                    f"• {existing_course.cours.nom} (début à {existing_course.start_time.strftime('%Hh%M')})\n"
                    f"• Votre cours finit à {end_time.strftime('%Hh%M')}"
                )

        # === 6. VALIDATION PROFESSEUR DISPONIBLE ===
        professeur = data.get('professeur')
        if professeur:
            if self.instance:
                prof_conflicts = Schedule.objects.filter(
                    day=day,
                    professeur=professeur
                ).exclude(id=self.instance.id)
            else:
                prof_conflicts = Schedule.objects.filter(day=day, professeur=professeur)

            for conflict in prof_conflicts:
                if (start_time < conflict.end_time and end_time > conflict.start_time):
                    raise serializers.ValidationError(
                        f"👨‍🏫 PROFESSEUR INDISPONIBLE !\n"
                        f"Le professeur {professeur} donne déjà un cours :\n"
                        f"• {conflict.cours.nom} en {conflict.salle.nom}\n"
                        f"• De {conflict.start_time.strftime('%Hh%M')} à {conflict.end_time.strftime('%Hh%M')}"
                    )

        return data

    def to_representation(self, instance):
        """Améliorer l'affichage des données"""
        representation = super().to_representation(instance)

        # Formater les heures pour l'affichage
        if instance.start_time:
            representation['start_time_display'] = instance.start_time.strftime('%Hh%M')
        if instance.end_time:
            representation['end_time_display'] = instance.end_time.strftime('%Hh%M')

        # Ajouter la durée du cours
        if instance.start_time and instance.end_time:
            duration = datetime.datetime.combine(datetime.date.today(), instance.end_time) - datetime.datetime.combine(
                datetime.date.today(), instance.start_time)
            representation['duration'] = f"{int(duration.total_seconds() / 60)} min"

        return representation