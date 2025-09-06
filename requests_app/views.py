from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Request
from .serializers import RequestSerializer, AdminRequestSerializer

# Étudiant : créer une demande et voir ses propres demandes
class StudentRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Request.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

# Admin : voir toutes les demandes
class AdminRequestListView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = AdminRequestSerializer
    permission_classes = [permissions.IsAdminUser]


# Admin : mettre à jour une demande spécifique (par ID)
class AdminRequestUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = AdminRequestSerializer
    permission_classes = [permissions.IsAdminUser]

