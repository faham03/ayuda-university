from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Event
from .serializers import EventSerializer


# Permission personnalisée
class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Permission qui permet:
    - Lecture pour tous les utilisateurs authentifiés
    - Écriture seulement pour le staff
    """

    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS autorisés pour tous les authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        # POST, PUT, DELETE seulement pour le staff
        return request.user.is_authenticated and request.user.is_staff


# Liste et création d'événements
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('start_date')
    serializer_class = EventSerializer
    permission_classes = [IsStaffOrReadOnly]  # ← CORRIGÉ !

    def get_queryset(self):
        """Filtrer les événements selon les paramètres"""
        queryset = Event.objects.all().order_by('start_date')

        # Filtre par type d'événement
        event_type = self.request.query_params.get('type', None)
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        # Filtre par événements à venir
        upcoming = self.request.query_params.get('upcoming', None)
        if upcoming:
            queryset = queryset.filter(start_date__gt=timezone.now())

        # Filtre par événements en cours
        ongoing = self.request.query_params.get('ongoing', None)
        if ongoing:
            now = timezone.now()
            queryset = queryset.filter(start_date__lte=now, end_date__gte=now)

        return queryset

    def create(self, request, *args, **kwargs):
        # Debug pour voir les infos de l'utilisateur
        print(f"=== DEBUG CRÉATION ÉVÉNEMENT ===")
        print(f"User: {request.user}")
        print(f"Is authenticated: {request.user.is_authenticated}")
        print(f"Is staff: {request.user.is_staff}")
        print(f"Is superuser: {request.user.is_superuser}")
        print(f"Data received: {request.data}")

        # Vérification manuelle des permissions
        if not request.user.is_staff:
            print("🚨 REFUSÉ : L'utilisateur n'est pas staff!")
            return Response(
                {"detail": "Vous n'avez pas la permission de créer un événement."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)


# Récupérer, modifier, supprimer un événement
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsStaffOrReadOnly]  # ← CORRIGÉ !

    def update(self, request, *args, **kwargs):
        # Debug pour voir les infos de l'utilisateur
        print(f"=== DEBUG MODIFICATION ÉVÉNEMENT ===")
        print(f"User: {request.user}")
        print(f"Is authenticated: {request.user.is_authenticated}")
        print(f"Is staff: {request.user.is_staff}")
        print(f"Data received: {request.data}")

        # Vérification manuelle des permissions
        if not request.user.is_staff:
            print("🚨 REFUSÉ : L'utilisateur n'est pas staff!")
            return Response(
                {"detail": "Vous n'avez pas la permission de modifier un événement."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Debug pour voir les infos de l'utilisateur
        print(f"=== DEBUG SUPPRESSION ÉVÉNEMENT ===")
        print(f"User: {request.user}")
        print(f"Is staff: {request.user.is_staff}")
        print(f"Event ID: {kwargs.get('pk')}")

        # Vérification manuelle des permissions
        if not request.user.is_staff:
            print("🚨 REFUSÉ : L'utilisateur n'est pas staff!")
            return Response(
                {"detail": "Vous n'avez pas la permission de supprimer un événement."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)