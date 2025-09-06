from rest_framework import generics,viewsets, permissions
from .models import Schedule
from .serializers import ScheduleSerializer

# Étudiants : voir l'emploi du temps
class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        filiere = self.request.query_params.get('filiere')
        year = self.request.query_params.get('year')
        day = self.request.query_params.get('day')

        queryset = Schedule.objects.all()

        if filiere:
            queryset = queryset.filter(filiere=filiere)
        if year:
            queryset = queryset.filter(year=year)
        if day:
            queryset = queryset.filter(day=day)

        return queryset



class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAdminUser]