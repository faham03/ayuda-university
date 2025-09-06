from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Grade
from .serializers import GradeSerializer

# Liste et création des notes
class GradeListCreateView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]  # Seul admin peut créer une note
        return [permissions.IsAuthenticated()]  # Tout étudiant peut voir

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # admin
            return Grade.objects.all()
        return Grade.objects.filter(student=user)


# Détail, modification et suppression
class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]  # Seul admin peut modifier
        return [permissions.IsAuthenticated()]  # Tout étudiant peut voir

