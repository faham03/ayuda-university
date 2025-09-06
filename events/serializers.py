from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    is_upcoming = serializers.ReadOnlyField()
    is_ongoing = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'event_type',
                  'start_date', 'end_date', 'is_upcoming', 'is_ongoing']

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("La date de début doit être avant la date de fin.")

        # Vérification de chevauchement avec d'autres événements
        overlapping = Event.objects.filter(
            start_date__lt=data['end_date'],
            end_date__gt=data['start_date']
        )
        if overlapping.exists():
            raise serializers.ValidationError("Un autre événement est déjà prévu sur ce créneau.")

        return data
