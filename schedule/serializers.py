from rest_framework import serializers
from .models import Schedule
from django.apps import apps
import datetime

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'filiere', 'year', 'day', 'course_name', 'professeur', 'salle', 'start_time', 'end_time']

    def validate(self, data):
        year = data.get('year')
        day = data.get('day')
        start = data.get('start_time')
        end = data.get('end_time')
        salle = data.get('salle')

        # Vérifier heure début < fin
        if start >= end:
            raise serializers.ValidationError("L'heure de début doit être avant l'heure de fin.")

        # Règles horaires par année
        if year in ['L1', 'L2']:
            morning_start = datetime.time(7, 30)
            morning_end = datetime.time(14, 30)
            if not (morning_start <= start < morning_end and morning_start < end <= morning_end):
                raise serializers.ValidationError("L1 et L2 : cours entre 07h30 et 14h30 uniquement.")
        elif year == 'L3':
            if day == 'samedi':
                sat_start = datetime.time(8, 0)
                sat_end = datetime.time(14, 0)
                if not (sat_start <= start < sat_end and sat_start < end <= sat_end):
                    raise serializers.ValidationError("L3 Samedi : cours entre 08h00 et 14h00 uniquement.")
            else:
                evening_start = datetime.time(19, 0)
                evening_end = datetime.time(21, 0)
                if not (evening_start <= start < evening_end and evening_start < end <= evening_end):
                    raise serializers.ValidationError("L3 (Lundi-Vendredi) : cours entre 19h00 et 21h00 uniquement.")

        # --- Vérification des conflits avec d'autres cours ---
        qs = Schedule.objects.filter(day=day, salle=salle)
        for c in qs:
            if self.instance and c.id == self.instance.id:
                continue  # Ignore le cours en cours de modification
            if (start < c.end_time and end > c.start_time):
                raise serializers.ValidationError(f"La salle {salle} est déjà occupée par {c.course_name} ({c.start_time}-{c.end_time}).")
            # Pause obligatoire de 30 minutes
            pause = datetime.timedelta(minutes=30)
            if abs(datetime.datetime.combine(datetime.date.today(), start) -
                   datetime.datetime.combine(datetime.date.today(), c.end_time)) < pause:
                raise serializers.ValidationError(f"La salle {salle} doit avoir une pause de 30 minutes entre les cours.")

        # --- Vérification des conflits avec événements académiques ---
        Event = apps.get_model('events', 'Event')
        conflicts = Event.objects.filter(
            location=salle,
            start_date__lt=datetime.datetime.combine(datetime.date.today(), end),
            end_date__gt=datetime.datetime.combine(datetime.date.today(), start),
            event_type="ACADEMIC"
        )
        if conflicts.exists():
            raise serializers.ValidationError(f"La salle {salle} est occupée par un événement académique ({conflicts.first().title}).")

        # --- Samedi : toutes les salles occupées ---
        if day == 'samedi':
            all_salles = [s[0] for s in Schedule.SALLE_CHOICES]
            salles_dispo = set(all_salles) - set(Schedule.objects.filter(day='samedi').values_list('salle', flat=True))
            if not salles_dispo:
                raise serializers.ValidationError("Toutes les salles sont occupées le samedi. Ce cours doit être reporté.")

        return data
