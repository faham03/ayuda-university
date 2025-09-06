from django.shortcuts import render
# reclamations/views.py
from rest_framework import viewsets, permissions
from .models import Reclamation
from .serializers import ReclamationSerializer

class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # L'admin peut tout voir/modifier
        if request.user.is_staff:
            return True
        # L'étudiant ne peut voir QUE ses réclamations
        return obj.student == request.user

class ReclamationViewSet(viewsets.ModelViewSet):
    serializer_class = ReclamationSerializer
    queryset = Reclamation.objects.all()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)  # auto-ajoute l’étudiant

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reclamation.objects.all()  # admin voit tout
        return Reclamation.objects.filter(student=self.request.user)  # étudiant voit seulement ses réclamations

