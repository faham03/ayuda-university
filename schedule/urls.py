from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScheduleListView, ScheduleViewSet,
    FiliereViewSet, CoursViewSet, SalleViewSet, AnneeViewSet
)

router = DefaultRouter()
# Configuration admin
router.register(r'filieres', FiliereViewSet, basename='filiere')
router.register(r'cours', CoursViewSet, basename='cours')
router.register(r'salles', SalleViewSet, basename='salle')
router.register(r'annees', AnneeViewSet, basename='annee')

# Schedule admin
router.register(r'schedule-admin', ScheduleViewSet, basename='schedule-admin')

urlpatterns = [
    # Consultation étudiants
    path('schedule/', ScheduleListView.as_view(), name='schedule-list'),

    # Configuration + CRUD admin
    path('', include(router.urls)),
]