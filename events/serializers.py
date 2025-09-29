from rest_framework import serializers
from django.utils import timezone
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    is_upcoming = serializers.ReadOnlyField()
    is_ongoing = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'event_type',
                  'start_date', 'end_date', 'created_at', 'is_upcoming', 'is_ongoing']

    def validate(self, data):
        # Validation des dates
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("La date de début doit être avant la date de fin.")

        # Validation de chevauchement CORRIGÉE
        start_date = data['start_date']
        end_date = data['end_date']

        # Exclure l'instance actuelle si on est en mode update
        instance = self.instance
        overlapping = Event.objects.filter(
            start_date__lt=end_date,
            end_date__gt=start_date
        )

        if instance:
            overlapping = overlapping.exclude(id=instance.id)

        if overlapping.exists():
            raise serializers.ValidationError(
                "Un autre événement est déjà prévu sur ce créneau."
            )

        return data