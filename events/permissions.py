from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializer

# Permission personnalisée
class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS autorisés pour tous les authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        # POST, PUT, DELETE seulement pour le staff
        return request.user.is_authenticated and request.user.is_staff

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('start_date')
    serializer_class = EventSerializer
    permission_classes = [IsStaffOrReadOnly]  # ← IMPORTANT

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsStaffOrReadOnly]  # ← IMPORTANT