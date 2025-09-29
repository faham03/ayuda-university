from rest_framework import generics, viewsets, permissions
from .models import Filiere, Cours, Salle, Annee, Schedule
from .serializers import (
    FiliereSerializer, CoursSerializer, SalleSerializer,
    AnneeSerializer, ScheduleSerializer
)


# === CONFIGURATION ADMIN ===
class FiliereViewSet(viewsets.ModelViewSet):
    queryset = Filiere.objects.all().order_by('nom')
    serializer_class = FiliereSerializer
    permission_classes = [permissions.IsAdminUser]


class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all().order_by('filiere', 'nom')
    serializer_class = CoursSerializer
    permission_classes = [permissions.IsAdminUser]


class SalleViewSet(viewsets.ModelViewSet):
    queryset = Salle.objects.all().order_by('nom')
    serializer_class = SalleSerializer
    permission_classes = [permissions.IsAdminUser]


class AnneeViewSet(viewsets.ModelViewSet):
    queryset = Annee.objects.all().order_by('nom')
    serializer_class = AnneeSerializer
    permission_classes = [permissions.IsAdminUser]


# === SCHEDULE ===
# Pour étudiants - consultation seulement
class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Schedule.objects.all()

        # Filtres
        filiere = self.request.query_params.get('filiere')
        annee = self.request.query_params.get('annee')
        day = self.request.query_params.get('day')

        if filiere:
            queryset = queryset.filter(filiere_id=filiere)
        if annee:
            queryset = queryset.filter(annee_id=annee)
        if day:
            queryset = queryset.filter(day=day)

        return queryset


# Pour admin - CRUD complet
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('day', 'start_time')
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAdminUser]