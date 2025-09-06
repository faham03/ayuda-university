from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializer

# Liste et création d'événements
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('start_date')
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]  # Seul admin peut créer
        return [permissions.AllowAny()]  # Tous peuvent consulter

# Récupérer, modifier, supprimer un événement
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]  # Seul admin modifie/supprime
        return [permissions.AllowAny()]

